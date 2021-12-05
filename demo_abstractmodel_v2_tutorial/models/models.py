from odoo import models, fields, api

class DemoMixin(models.AbstractModel):
    _name = 'demo.mixin'
    _description = 'Demo Mixin'

    test_1 = fields.Float(
        string='test_1',
        default='2.2'
    )

    test_2 = fields.Float(
        string="test_2",
        compute="_compute_field",
    )

    def _compute_field(self):
        for record in self:
            record.test_2 = 3.0

class DemoModelTutorial(models.Model):
    _name = 'demo.model.tutorial'
    _inherit = 'demo.mixin'
    _description = 'Demo Model Tutorial'

    name = fields.Char(required=True, string="名稱")
