# -*- coding: utf-8 -*-
{
    'name': "Engineering Sales",

    'summary': "Automates the creation of projects from sales orders.",

    'description': """
        This module extends the Sales application to automatically create a
        new project in the Project app when a sales order is confirmed.
    """,

    'author': "Your Name",
    'website': "https://www.yourcompany.com",

    'category': 'Sales/Sales',
    'version': '17.0.1.0.0',

    # CRITICAL: Add dependencies on sale_management and project
    'depends': ['sale_management', 'project'],

    # We will create this python file in the next step
    'data': [], # No XML views are needed for this part

    'installable': True,
    'application': False,
    'auto_install': False,
}