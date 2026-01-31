# -*- coding: utf-8 -*-
{
    'name': "Engineering Supervision",

    'summary': "Manages site visit reports for engineering projects.",

    'description': """
        - Creates a new model to store site visit reports.
        - Provides a form for creating new reports.
        - Adds a menu item to access the reports.
    """,

    'author': "Your Name",
    'website': "https://www.yourcompany.com",

    'category': 'Services/Project',
    'version': '17.0.1.0.0',

    'depends': ['project'],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml', # <-- ADD THIS LINE
        'report/site_visit_report_templates.xml',  # <-- ADD THIS
        'report/site_visit_report_action.xml',   # <-- ADD THIS
        'views/site_visit_report_views.xml',
        'views/menus.xml',
    ],

    'installable': True,
    'application': False,
}
