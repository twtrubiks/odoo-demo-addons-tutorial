{
    'name': "demo_js_iframe_tutorial",
    'summary': """
        demo_js_iframe_tutorial
    """,
    'description': """
        demo_js_iframe_tutorial
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': "17.0.0.0.0",
    'depends': ['web', 'base'],
    'data': [
        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'demo_js_iframe_tutorial/static/src/**/*',
            'demo_js_iframe_tutorial/static/src/xml/**/*',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}