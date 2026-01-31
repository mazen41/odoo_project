from odoo import models, fields, api
from odoo.tools import date_utils

class ProjectProject(models.Model):
    _inherit = 'project.project'

    currency_id = fields.Many2one(
        'res.currency',
        related="company_id.currency_id",
        string="Currency",
        store=True,
        readonly=True,
    )
    extra_month_cost = fields.Monetary(
        string="Extra Supervision Cost (Monthly)",
        currency_field='currency_id'
    )
    supervision_end_date = fields.Date(string="Planned Supervision End Date")
    last_extra_invoice_date = fields.Date(string="Last Extra Invoice Date", readonly=True)

    # ---------------------------------------------------------
    # WRITE OVERRIDE
    # ---------------------------------------------------------
    def write(self, vals):
        if self.env.context.get('skip_stage_logic'):
            return super().write(vals)

        res = super().write(vals)

        if 'stage_id' in vals:
            arch_design_stage = self.env.ref('engineering_project_stage_arch_design', raise_if_not_found=False)
            contracting_stage = self.env.ref('engineering_project_stage_contract_creation', raise_if_not_found=False)

            for project in self:
                tasks_to_create = []

                if arch_design_stage and project.stage_id.id == arch_design_stage.id:
                    task_sketch = self.env.ref('engineering_project.task_template_prepare_sketch', raise_if_not_found=False)
                    if task_sketch:
                        tasks_to_create.append({
                            'name': task_sketch.sudo().name,
                            'project_id': project.id,
                            'user_ids': [(6, 0, [project.user_id.id])] if project.user_id else False,
                        })

                elif contracting_stage and project.stage_id.id == contracting_stage.id:
                    task_contract = self.env.ref('engineering_project.task_template_prepare_contract', raise_if_not_found=False)
                    task_payment = self.env.ref('engineering_project.task_template_follow_payment', raise_if_not_found=False)
                    task_docs = self.env.ref('engineering_project.task_template_request_docs', raise_if_not_found=False)

                    if task_contract:
                        tasks_to_create.append({'name': task_contract.sudo().name, 'project_id': project.id})
                    if task_payment:
                        tasks_to_create.append({'name': task_payment.sudo().name, 'project_id': project.id})
                    if task_docs:
                        tasks_to_create.append({'name': task_docs.sudo().name, 'project_id': project.id})

                if tasks_to_create:
                    self.env['project.task'].sudo().create(tasks_to_create)

        return res

    # ---------------------------------------------------------
    # CREATE OVERRIDE
    # ---------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        projects = super().create(vals_list)

        stage_ids = [
            self.env.ref('engineering_project.engineering_project_stage_new').id,
            self.env.ref('engineering_project.engineering_project_stage_doc_collection').id,
            self.env.ref('engineering_project.engineering_project_stage_contract_creation').id,
            self.env.ref('engineering_project.engineering_project_stage_arch_design').id,
            self.env.ref('engineering_project.engineering_project_stage_struct_design').id,
            self.env.ref('engineering_project.engineering_project_stage_municipality_sub').id,
            self.env.ref('engineering_project.engineering_project_stage_supervision_pledge').id,
            self.env.ref('engineering_project.engineering_project_stage_on_site_supervision').id,
            self.env.ref('engineering_project.engineering_project_stage_completed').id,
            self.env.ref('engineering_project.engineering_project_stage_archived').id,
        ]


        for project in projects:
            if not project.type_ids:
                project.sudo().with_context(skip_stage_logic=True).write({
                    'stage_id': self.env.ref('engineering_project.engineering_project_stage_new').id,
                    'type_ids': [(4, sid) for sid in stage_ids],
                })

        return projects

    # ---------------------------------------------------------
    # CRON BILLING
    # ---------------------------------------------------------
    def _cron_check_supervision_billing(self):
        today = fields.Date.today()

        overdue_projects = self.search([
            ('supervision_end_date', '!=', False),
            ('supervision_end_date', '<', today),
            ('extra_month_cost', '>', 0),
            '|',
            ('last_extra_invoice_date', '=', False),
            ('last_extra_invoice_date', '<', today - date_utils.relativedelta(days=30))
        ])

        for project in overdue_projects:
            if not project.partner_id:
                continue

            invoice = self.env['account.move'].sudo().create({
                'move_type': 'out_invoice',
                'partner_id': project.partner_id.id,
                'currency_id': project.currency_id.id,
                'invoice_date': today,
                'invoice_line_ids': [(0, 0, {
                    'name': f'Extra Supervision for {project.name} - {today.strftime("%B %Y")}',
                    'quantity': 1,
                    'price_unit': project.extra_month_cost,
                })],
            })

            project.sudo().write({'last_extra_invoice_date': today})
            project.message_post(body=f"An extra supervision invoice has been automatically generated: {invoice.name}")

        return True
