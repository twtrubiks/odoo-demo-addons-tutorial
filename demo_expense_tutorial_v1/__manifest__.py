{
    'name': "demo expense tutorial v1",
    'summary': """
        tutorial
    """,
    'description': """
        tutorial
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': "18.0.0.1",
    'depends': ['base', 'hr', 'analytic'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'data/analytic_account_data.xml',
        'data/demo_expense_tutorial_data.xml',
        'views/view.xml',
        'views/menu.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
