from odoo import models, fields, api

class DemoSequence(models.Model):
    _name = 'demo.sequence'
    _description = 'Demo Sequence'

    name = fields.Char(string='Name', required=True)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('demo.sequence') or '/'
        vals['name'] = '{}_{}'.format(seq, vals['name'])
        new_record = super().create(vals)
        return new_record
