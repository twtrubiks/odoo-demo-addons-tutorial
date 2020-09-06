from odoo import models, fields, api

# ref.
#
# addons/product/models/product.py
# class ProductProduct(models.Model):
#   _name = "product.product"
#
# addons/product/models/product_template.py
# class ProductTemplate(models.Model):
#   _name = "product.template"
#

class DelegationInheritance(models.Model):
    _name = 'demo.delegation'
    _description = 'Demo DelegationInheritance'
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete="cascade")

    first_name = fields.Char('First Name', size=16)
