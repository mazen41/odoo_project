import base64
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class SiteVisitReport(models.Model):
    _name = 'site.visit.report'
    _description = 'Site Visit Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Fields
    name = fields.Char(string='Report Number', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    project_id = fields.Many2one('project.project', string='Project', required=True, ondelete='cascade')
    visit_date = fields.Date(string='Visit Date', required=True, default=fields.Date.context_today)
    attendees_ids = fields.Many2many('res.partner', string='Attendees')
    observations = fields.Html(string='Observations')
    image = fields.Image(string='Site Photo')

    # === REVISED AND BULLETPROOF CREATE METHOD ===
    @api.model_create_multi
    def create(self, vals_list):
        # The @api.model_create_multi decorator ensures vals_list is always a list of dicts.
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('site.visit.report') or _('New')

        # Call super to actually create the records
        records = super(SiteVisitReport, self).create(vals_list)

        # Send email for each newly created record
        for rec in records:
            try:
                # Use with_delay() to send the email in a background job.
                # This prevents the user from having to wait and avoids errors if the email fails.
                rec.with_delay()._send_report_by_email()
                _logger.info("Successfully queued email for site visit report %s.", rec.name)
            except Exception as e:
                _logger.error("Failed to queue site visit report email for report %s: %s", rec.name, e)

        return records

    # === EMAIL SENDING METHOD (UNCHANGED) ===
    def _send_report_by_email(self):
        self.ensure_one()
        _logger.info("BACKGROUND JOB: Sending site visit report email for report: %s", self.name)

        if not self.project_id:
            _logger.warning("No project linked to report %s. Cannot send email.", self.name)
            return False
        if not self.project_id.partner_id:
            _logger.warning("Project %s has no partner linked. Cannot send email for report %s.", self.project_id.name, self.name)
            return False
        if not self.project_id.partner_id.email:
            _logger.warning(
                "Partner %s has no email address. Cannot send email for report %s.",
                self.project_id.partner_id.name,
                self.name
            )
            return False

        report = self.env.ref('engineering_supervision.action_report_site_visit')
        if not report:
            _logger.error("Report 'engineering_supervision.action_report_site_visit' not found!")
            return False

        # Render PDF
        try:
            pdf_content, _ = report._render_qweb_pdf(self.id)
            _logger.info("PDF content rendered successfully for report: %s", self.name)
        except Exception as e:
            _logger.error("Failed to render PDF for report %s: %s", self.name, e)
            return False

        # Create attachment
        try:
            attachment = self.env['ir.attachment'].create({
                'name': _("Site Visit Report - %s.pdf") % self.name,
                'type': 'binary',
                'datas': base64.b64encode(pdf_content),
                'mimetype': 'application/pdf',
                'res_model': self.project_id._name,
                'res_id': self.project_id.id,
            })
            _logger.info("Attachment created successfully for report: %s", self.name)
        except Exception as e:
            _logger.error("Failed to create attachment for report %s: %s", self.name, e)
            return False

        # Post message/email
        try:
            self.project_id.message_post(
                subject=_("Site Visit Report: %s") % self.name,
                body=_(
                    "Dear %s,<br/><br/>"
                    "A new site visit report has been logged for your project. "
                    "Please find it attached.<br/><br/>Thank you."
                ) % self.project_id.partner_id.name,
                partner_ids=[self.project_id.partner_id.id],
                attachment_ids=[attachment.id],
                message_type='email',
                subtype_xmlid='mail.mt_comment',
            )
            _logger.info(
                "Email for report %s successfully posted to partner %s.",
                self.name,
                self.project_id.partner_id.email
            )
        except Exception as e:
            _logger.error("Failed to post message for report %s: %s", self.name, e)
            return False

        return True