from odoo import models, fields


class DemoLineTutorial(models.Model):
    _name = 'demo.line.tutorial'
    _description = 'Demo Line Tutorial'

    line_id = fields.Many2one('demo.domain.tutorial', string="Demo Domain", ondelete='restrict')
    product_id = fields.Many2one('product.product', string="Product")

class DemoDomainTutorial(models.Model):
    _name = 'demo.domain.tutorial'
    _description = 'Demo Domain Tutorial'

    name = fields.Char('Description', required=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    product_id = fields.Many2one('product.product', string="Product",
        domain="[('seller_ids.partner_id', '=', partner_id)]")
    taxes_ids = fields.Many2many('account.tax', string='Taxes')
    line_ids = fields.One2many(
        'demo.line.tutorial', # related model
        'line_id', # field for "this" on related model
        string='Demo Lines')
