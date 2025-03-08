from odoo import models, fields


class DemoTutorial(models.Model):
    _name = 'demo.tutorial'
    _description = 'Demo Tutorial'

    name = fields.Char('Description', required=True)
    sheet_id = fields.Many2one('demo.sheet.tutorial', string="Sheet", ondelete='restrict')

    def action_open_sheet(self):
        self.ensure_one()
        if self.sheet_id:
            return {
                'res_model': self.sheet_id._name,
                'type': 'ir.actions.act_window',
                'views': [[False, "form"]],
                'res_id': self.sheet_id.id,
            }
        return {
            'res_model': self._name,
            'type': 'ir.actions.act_window',
            'views': [[False, "form"]],
            'res_id': self.id,
        }

class DemoSheetTutorial(models.Model):
    _name = 'demo.sheet.tutorial'
    _description = 'Demo Sheet Tutorial'

    name = fields.Char('Demo Sheet Summary', required=True)

    sheet_line_ids = fields.One2many(
        'demo.tutorial', # related model
        'sheet_id', # field for "this" on related model
        string='Sheet Lines')

