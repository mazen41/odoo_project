# -*- coding: utf-8 -*-
{
    'name': "Engineering CRM",
    'summary': "Customizations for engineering-specific CRM processes.",
    'author': "Your Name",
    'website': "https://www.yourcompany.com",
    'category': 'Sales/CRM',
    'version': '17.0.1.0.0',
    'depends': ['crm'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
}