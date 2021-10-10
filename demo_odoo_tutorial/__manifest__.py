{
    'name': "demo odoo tutorial",
    'summary': """
        basic tutorial -
        demo odoo tutorial
    """,
    'description': """
        basic tutorial -
        demo odoo tutorial
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'website'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data_demo_odoo.xml',
        'views/menu.xml',
        'views/view.xml',
        'reports/report.xml',
        'views/demo_odoo_template.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
