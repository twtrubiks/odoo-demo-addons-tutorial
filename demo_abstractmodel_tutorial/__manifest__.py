{
    'name': "demo_abstractmodel_tutorial",
    'summary': """
        AbstractModel report
    """,
    'description': """
        AbstractModel report
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_expense'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/model_wizard.xml',
        'reports/report.xml'
    ],
    'application': True,
}
