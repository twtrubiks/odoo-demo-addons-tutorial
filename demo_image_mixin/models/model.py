from odoo import models, fields, api

class DemoImage(models.Model):
    _name = 'demo.image'
    _description = 'Demo Image'
    _inherit = ['image.mixin']

    name = fields.Char(string='Name', required=True)
    # image_1920 = fields.Image(required=True)
