from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.misc import clean_context

class DemoOdooWizardTutorial(models.Model):
    _name = 'demo.odoo.wizard.tutorial'
    _description = 'Demo Odoo Wizard Tutorial'

    name = fields.Char('Description', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    uid = fields.Char(compute='_compute_uid')
    lang = fields.Char(compute='_compute_lang')

    @api.depends_context('uid')
    def _compute_uid(self):
        context = clean_context(self.env.context)
        for rec in self:
            rec.uid = context.get('uid')

    @api.depends_context('lang')
    def _compute_lang(self):
        context = clean_context(self.env.context)
        for rec in self:
            rec.lang = context.get('lang')

    def action_context_demo(self):
        context = clean_context(self.env.context)
        if context.get('context_data'):
            raise ValidationError('have context data')
        raise ValidationError('hello')

    def action_button(self):
        for record in self:
            record.with_context(context_data=True).action_context_demo()