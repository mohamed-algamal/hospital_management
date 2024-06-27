{
    'name': 'hospital management',
    'version': '1.0.0',
    'category': 'hospital',
    'author': 'mohamed algamal',
    'summary': 'hospital management task',
    'description': """hospital management task""",
    'depends': ['base', 'mail',],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        # 'data/mail_template_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/menu_view.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/medication.xml',
        # 'report/report.xml',

    ],
    'demo': [],
    'sequence': -100,
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
# -*- coding: utf-8 -*-
