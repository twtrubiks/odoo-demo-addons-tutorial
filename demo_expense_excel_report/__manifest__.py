{
    'name': "demo_expense_excel_report",
    'summary': """
        tutorial
    """,
    'description': """
        tutorial
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': "16.0.0.0.0",
    'depends': ['hr_expense',],
    'data': [
        'views/hr_expense_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'demo_expense_excel_report/static/src/js/action_excel_report.js',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}
