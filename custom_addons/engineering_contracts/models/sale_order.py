import base64
from odoo import models, fields, _
from odoo.exceptions import UserError
import urllib.parse

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _find_report(self):
        report_name = 'engineering_contracts.report_contract_template'
        report = self.env['ir.actions.report'].search(
            [('report_name', '=', report_name)], limit=1
        )
        if not report:
            raise UserError(_(f"The report '{report_name}' could not be found."))
        return report

    def action_print_contract(self):
        report = self._find_report()
        return report.report_action(self)

    def action_send_contract_email(self):
        self.ensure_one()

        report = self._find_report()

        # 1. Render PDF
        pdf_content, _content_type = report._render_qweb_pdf(report.report_name, self.ids)

        # 2. Create attachment
        attachment = self.env['ir.attachment'].create({
            'name': f"Contract - {self.name}.pdf",
            'datas': base64.b64encode(pdf_content),
            'type': 'binary',
            'mimetype': 'application/pdf',
            'res_model': self._name,
            'res_id': self.id,
        })

        # 3. Post message with attachment
        self.message_post(
            body=f"Dear {self.partner_id.name},<br/><br/>Please find your contract attached.<br/><br/>Thank you.",
            attachment_ids=[attachment.id],
        )

        return True

    def action_send_contract_whatsapp(self):
        self.ensure_one()
        # The 'mobile' field is on res.partner, which partner_id links to.
        # Odoo handles partner_id.mobile traversal for the phone number.
        if not self.partner_id.mobile and not self.partner_id.phone:
            raise UserError(_("Customer has no mobile or phone number configured."))
        
        customer_phone = self.partner_id.mobile or self.partner_id.phone
        
        # Remove any non-digit characters from the phone number
        customer_phone = ''.join(filter(str.isdigit, customer_phone))
        
        # Base WhatsApp URL. You can customize the message.
        message = _("Please review the attached quotation for your project: %s. Thank you." % self.name)
        whatsapp_url = f"https://wa.me/{customer_phone}?text={urllib.parse.quote(message)}"
        
        # This action will redirect the user's browser to the WhatsApp link
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new', # Open in a new tab
        }