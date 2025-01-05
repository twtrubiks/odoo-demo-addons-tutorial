{
    'name': "demo domain x2many tutorial",
    'summary': """
        tutorial
    """,
    'description': """
        tutorial
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': "17.0.0.0.0",
    'depends': ['purchase', 'account', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'views/menu.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
