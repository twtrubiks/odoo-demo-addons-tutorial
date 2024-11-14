from odoo import models, fields, api

class DemoSequence(models.Model):
    _name = 'demo.sequence'
    _description = 'Demo Sequence'

    name = fields.Char(string='Name', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            seq = self.env['ir.sequence'].next_by_code('demo.sequence') or '/'
            vals['name'] = f'{seq}_{vals["name"]}_{self.env.company.name}'
        return super().create(vals_list)