from odoo import http, _
from odoo.http import request
import json

class DemoApiController(http.Controller):
    def get_res_users(self, pk=None):
        if pk:
            domain = [("id", "=", pk)]
        else:
            domain = []

        return [
            {
                "id": record.id,
                "name": record.name,
                "company": record.company_id.name,
                "phone": record.phone,
                "email": record.email,
            }
            for record in request.env["res.users"].sudo().search(domain)
        ]

    @http.route("/api/users/<string:pk>", methods=["GET"], type="json", auth="user")
    def api_get_res_users(self, pk=None):
        return json.dumps(self.get_res_users(pk))

    @http.route("/api/users/", methods=["GET"], type="json", auth="user")
    def api_get_res_user(self):
        return json.dumps(self.get_res_users())

    @http.route("/api/users/", methods=["POST"], type="json", auth="user")
    def api_post_res_user(self):
        param = request.jsonrequest

        if not param["login"]:
            return json.dumps("login not allow empty")

        vals = {
            "name": param["name"],
            "phone": param["phone"],
            "email": param["email"],
            "login": param["login"],
        }
        if request.env["res.users"].sudo().search([("login", "=", param["login"])]):
            return json.dumps("already exists")

        res_user = request.env["res.users"].sudo().create(vals)
        return json.dumps(self.get_res_users(res_user.id))

    @http.route("/api/users/<string:pk>", methods=["PATCH"], type="json", auth="user")
    def api_patch_res_user(self, pk=None):
        param = request.jsonrequest
        res_user = request.env["res.users"].sudo().search([("id", "=", pk)])
        if not res_user:
            return json.dumps("not exists")

        res_user.phone = param["phone"]
        return json.dumps(self.get_res_users(pk))