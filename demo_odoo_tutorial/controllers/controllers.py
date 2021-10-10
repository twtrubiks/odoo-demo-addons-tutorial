from odoo import http

class DemoOdoo(http.Controller):

    @http.route('/demo/odoo', auth='user', website=True)
    def list(self, **kwargs):
        obj = http.request.env['demo.odoo.tutorial']
        objs = obj.search([])
        print(http.request.website.id)
        return http.request.render(
            'demo_odoo_tutorial.demo_odoo_template',{'objs': objs})
