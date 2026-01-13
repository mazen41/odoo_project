from odoo import models, fields

class CrmLead(models.Model):
    """
    This class inherits the crm.lead model to add fields specific to the
    engineering business flow.
    """
    _inherit = 'crm.lead' # This is the crucial line to extend an existing model

    # --- Field Definitions ---

    building_type = fields.Selection([
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('other', 'Other'),
    ], string='Building Type', default='residential', required=True)

    service_type = fields.Selection([
        ('consultation', 'Consultation'),
        ('design', 'Design'),
        ('supervision', 'Supervision'),
        ('full_package', 'Full Package'),
    ], string='Service Type', required=True)

    site_info = fields.Text(string='Site Information / Address')