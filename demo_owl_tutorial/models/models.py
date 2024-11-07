from odoo import models, fields, api

class DemoOWLTutorial(models.Model):
    _name = 'demo.owl.tutorial'
    _description = 'Demo OWL Tutorial'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Description', required=True)
    user_id = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user)

    def call_odoo_method(self):
        return "成功被 js 呼叫了"
