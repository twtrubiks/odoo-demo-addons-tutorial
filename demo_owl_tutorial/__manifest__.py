{
    'name': "demo_owl_tutorial",
    'summary': """
        owl tutorial
    """,
    'description': """
        owl tutorial
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': "17.0.0.0.0",
    'depends': ['web', 'base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'demo_owl_tutorial/static/src/xml/custom_button_widget.xml',
            'demo_owl_tutorial/static/src/js/custom_button_widget.js',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}
