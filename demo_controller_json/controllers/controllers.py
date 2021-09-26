from odoo import http, _
from odoo.http import request
import json

class DemoController(http.Controller):

    @http.route('/get_res_users/type1', type='http', auth='none')
    def get_res_users_http(self):

        data = [
            {
                'id': record.id,
                'name': record.name,
                'company': record.company_id.name,
                'phone': record.phone,
                'email': record.email,
            }
            for record in request.env['res.users'].sudo().search([])
            ]

        return json.dumps(data)

    @http.route('/get_res_users/type2', type='json', auth='none')
    def get_res_users_json(self):
        data = [
            {
                'id': record.id,
                'name': record.name,
                'company': record.company_id.name,
                'phone': record.phone,
                'email': record.email,
            }
            for record in request.env['res.users'].sudo().search([])
            ]

        return json.dumps(data)





