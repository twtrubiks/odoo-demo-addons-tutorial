{
    'name': "demo_js_class_tutorial",
    'summary': """
        js_class tutorial
    """,
    'description': """
        js_class tutorial
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': "17.0.0.0.0",
    'depends': ['web', 'base', 'hr_expense'],
    'data': [
        'views/hr_expense_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'demo_js_class_tutorial/static/src/xml/js_custom_dialog.xml',
            'demo_js_class_tutorial/static/src/js/js_custom_dialog.js',

            'demo_js_class_tutorial/static/src/xml/custom_info_form_button.xml',
            'demo_js_class_tutorial/static/src/js/custom_info_form_button.js',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}
