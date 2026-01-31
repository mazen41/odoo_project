# -*- coding: utf-8 -*-
{
    'name': "Engineering Project",

    'summary': "Automates the creation of standard stages and tasks for engineering projects.",

    'description': """
        When a project is created, this module automatically populates it
        with a predefined template of stages (e.g., Planning, Execution, Supervision).
    """,

    'author': "Your Name",
    'website': "https://www.yourcompany.com",

    'category': 'Services/Project',
    'version': '17.0.1.0.0',

    # This module depends on the main project app
    'depends': ['project'],

    # We need to load our new data file
    'data': [
        'data/project_stage_data.xml',
        'data/project_task_data.xml', # <-- ADD THIS NEW LINE
            'data/project_cron_data.xml',      # <-- ADD THIS
    'views/project_project_views.xml', # <-- ADD THIS


    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}