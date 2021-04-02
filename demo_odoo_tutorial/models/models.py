from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class DemoOdooTutorial(models.Model):
    _name = 'demo.odoo.tutorial'
    _description = 'Demo Odoo Tutorial'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # track_visibility

    name = fields.Char('Description', required=True)

    # track_visibility='always' 和 track_visibility='onchange'
    is_done_track_onchange = fields.Boolean(
        string='Is Done?', default=False, track_visibility='onchange')
    name_track_always = fields.Char(string="track_name", track_visibility='always')

    start_datetime = fields.Datetime('Start DateTime', default=fields.Datetime.now())
    stop_datetime = fields.Datetime('End Datetime', default=fields.Datetime.now())

    field_onchange_demo = fields.Char('onchange_demo')
    field_onchange_demo_set = fields.Char('onchange_demo_set', readonly=True)

    # float digits
    # field tutorial
    input_number = fields.Float(string='input number', digits=(10,3))
    field_compute_demo = fields.Integer(compute="_get_field_compute") # readonly

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Description must be unique'),
    ]

    @api.constrains('start_datetime', 'stop_datetime')
    def _check_date(self):
        for data in self:
            if data.start_datetime > data.stop_datetime:
                raise ValidationError(
                    "data.stop_datetime  > data.start_datetime"
                )

    @api.depends('input_number')
    def _get_field_compute(self):
        for data in self:
            data.field_compute_demo = data.input_number * 1000

    @api.onchange('field_onchange_demo')
    def onchange_demo(self):
        if self.field_onchange_demo:
            self.field_onchange_demo_set = 'set {}'.format(self.field_onchange_demo)

        # warning message
        result = dict()
        result['warning'] = {
            'title': 'HELLO',
            'message': 'I am warning'
        }
        return result
