# -*- coding: utf-8 -*-
{
    'name': 'Minutes of Meeting',
    'version': '19.0.1.0.0',
    'category': 'Project',
    'summary': 'Record and manage Minutes of Meeting with clients for software development projects',
    'description': """
        Minutes of Meeting (MOM) Module
        ================================
        - Record meeting minutes with client details
        - Track meeting participants
        - Link meetings to projects (Web / ERP)
        - Log discussion points, requirements, and action items
        - Print/PDF report per meeting date
    """,
    'author': 'Your Company',
    'depends': ['base', 'mail', 'project', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/mom_sequence.xml',
        'views/mom_meeting_views.xml',
        'views/mom_menu.xml',
        'report/mom_report_template.xml',
        'report/mom_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
