# -*- coding: utf-8 -*-
{
    'name': "Engineering Contracts",

    'summary': "Generates and emails client contracts for engineering projects.",

    'description': """
        - Adds a button to the Sales Order to print a dynamic contract.
        - Adds a button to email the contract PDF to the client.
    """,

    'author': "Your Name",
    'website': "https://www.yourcompany.com",

    'category': 'Sales/Sales',
    'version': '17.0.1.0.0',

    # We ONLY depend on Sales now.
    'depends': ['sale_management', 'contacts'],

    'data': [
        'views/sale_order_views.xml',
        'report/contract_report_templates.xml',
        'report/contract_report.xml',
    ],

    'installable': True,
    'application': False,
}