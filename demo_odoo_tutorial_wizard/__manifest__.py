{
    'name': "demo odoo tutorial wizard",
    'summary': """
        wizard tutorial -
        demo odoo tutorial wizard
    """,
    'description': """
        wizard tutorial -
        demo odoo tutorial wizard
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': "16.0.1.0.0",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/model_wizard.xml',
        'views/menu.xml',
        'views/view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
