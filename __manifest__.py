# -*- coding: utf-8 -*-
{
    'name': "User Audit",

    'description': """
    
    -1- Easy to track all operations performed by users.
    -2- Users can view only the user audit log list.
    -3- Operations performed by a user will automatically record in the logs list.

    """,

    'author': "",
    'category': '',
    'version': '0.1',

    'depends': ['crm',
                'purchase',
                'hr'
                ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'data/cron.xml',
        'wizard/user_audit_clear_log.xml',
        'views/user_audit_log.xml',
        'views/res_config.xml',
        'views/menu.xml',
    ],
}
