from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # --- UPDATED FIELD ---
    building_type = fields.Selection([
        ('private_residence', 'Private Residence (سكن خاص)'),
        ('investment', 'Investment (استثماري)'),
        ('commercial', 'Commercial (تجاري)'),
        ('industrial', 'Industrial (صناعي)'),
        ('society', 'Society (جمعيات)'),
        ('mosque', 'Mosque (مساجد)'),
        ('hanger', 'Hangar (هنجر)'),
        ('farm', 'Farm (مزارع)'),
        ('other', 'Other'),
    ], string='Building Type', required=True, default='private_residence')

    # --- COMPLETELY REVISED FIELD ---
    license_type = fields.Selection([
        ('new_build', 'New Build (بناء جديد)'),
        ('modification', 'Modification (تعديل)'),
        ('addition', 'Addition (إضافة)'),
        ('mod_add', 'Modification & Addition (تعديل وإضافة)'),
        ('demolition', 'Demolition (هدم)'),
        ('restoration', 'Restoration (ترميم)'),
        ('other', 'Other'),
    ], string='License Type', required=True, default='new_build')

    # --- NEW FIELDS FROM THE REQUIREMENTS ---
    site_land_area = fields.Float(string="Land Area (m²)")
    site_plot_number = fields.Char(string="Plot Number")
    