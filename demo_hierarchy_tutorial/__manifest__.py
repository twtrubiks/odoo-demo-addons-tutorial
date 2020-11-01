{
    'name': "demo hierarchy tutorial",
    'summary': """
        demo_hierarchy_tutorial
    """,
    'description': """
        demo_hierarchy_tutorial
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
