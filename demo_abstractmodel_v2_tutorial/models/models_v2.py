from odoo import models, fields, api

class DemoMixin2(models.AbstractModel):
    _name = 'demo.mixin2'
    _description = 'Demo Mixin2'

    test_v2 = fields.Float(
        string='test_v2',
        default='2.2'
    )

class DemoModelTutorial(models.Model):
    _name = 'demo.model.tutorial'
    _inherit = ['demo.model.tutorial', 'demo.mixin2']

    pass
