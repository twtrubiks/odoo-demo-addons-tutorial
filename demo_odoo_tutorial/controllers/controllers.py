from odoo import http


class DemoOdoo(http.Controller):

    @http.route('/demo/odoo', auth='user')
    def list(self, **kwargs):
        obj = http.request.env['demo.odoo.tutorial']
        objs = obj.search([])
        return http.request.render(
            'demo_odoo_tutorial.demo_odoo_template',{'objs': objs})
