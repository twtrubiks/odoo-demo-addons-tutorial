{
    'name': "demo multi company sequence",
    'summary': """""",

    'description': """""",

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': "17.0.0.0.0",

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/data.xml',
        'views/view.xml',
        'views/menu.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
