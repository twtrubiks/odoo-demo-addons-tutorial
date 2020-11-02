from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DemoOdooWizardTutorial(models.Model):
    _name = 'demo.odoo.wizard.tutorial'
    _description = 'Demo Odoo Wizard Tutorial'

    name = fields.Char('Description', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')

    def action_context_demo(self):
        # if self._context.get('context_data', False):
        if self.env.context.get('context_data'):
            raise ValidationError('have context data')
        raise ValidationError('hello')

    def action_button(self):
        for record in self:
            record.with_context(context_data=True).action_context_demo()