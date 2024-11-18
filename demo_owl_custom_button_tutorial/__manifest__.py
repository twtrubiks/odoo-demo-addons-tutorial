{
    'name': "demo_owl_custom_button_tutorial",
    'summary': """
        owl tutorial
    """,
    'description': """
        owl tutorial
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': "16.0.1.0.0",
    'depends': ['web', 'base', 'mail', 'hr_expense'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'demo_owl_custom_button_tutorial/static/src/xml/custom_form_button.xml',
            'demo_owl_custom_button_tutorial/static/src/js/custom_form_button.js',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}
