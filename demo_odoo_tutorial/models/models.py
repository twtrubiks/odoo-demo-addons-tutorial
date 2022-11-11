from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from datetime import datetime

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

    # field_compute_demo = fields.Integer(compute="_get_field_compute",
    #                                     inverse="_set_input_number",
    #                                     search="_search_upper")

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

    def _set_input_number(self):
        for data in self:
            data.input_number = data.field_compute_demo / 1000

    def _search_upper(self, operator, value):
        return [('input_number', operator, value)]

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

    def demo_raw_sql(self):
        query = """
            SELECT
                id, name,
                is_done_track_onchange,
                name_track_always,
                start_datetime,
                stop_datetime,
                field_onchange_demo,
                field_onchange_demo_set,
                input_number
	        FROM
                demo_odoo_tutorial;
        """
        self.env.cr.execute(query)

        print('self.env.cr.fetchall:', self.env.cr.fetchall())
        # print('self.env.cr.fetchone:', self.env.cr.fetchone())
        # print('self.env.cr.dictfetchall:', self.env.cr.dictfetchall())


        # query = """
        #     SELECT
        #         id, name,
        #         is_done_track_onchange,
        #         name_track_always,
        #         start_datetime,
        #         stop_datetime,
        #         field_onchange_demo,
        #         field_onchange_demo_set,
        #         input_number
        # FROM
        #         demo_odoo_tutorial
        # WHERE
        #         name like %s and 1 = %s;
        # """

        # query_sql_params = ('%%odoo%%', 1,)
        # # query_sql_params = ('%odoo%', 1,)
        # self.env.cr.execute(query)

    def get_custom_portal_date(self):
        str_time = datetime.strftime(self.start_datetime, '%Y/%m/%d')
        return '>{}<'.format(str_time)

class DemoOdooTutorialStatistics(models.Model):
    _name = 'demo.odoo.tutorial.statistics'
    _description = 'Demo Odoo Tutorial Statistics'
    _auto = False

    create_uid = fields.Many2one('res.users', 'Created by', readonly=True)
    average_input_number = fields.Float(string="Average Input Number", readonly=True)

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
        CREATE OR REPLACE VIEW demo_odoo_tutorial_statistics AS
        (
            SELECT
                min(demo.id) as id,
                create_uid,
                avg(input_number) AS average_input_number
            FROM
                demo_odoo_tutorial AS demo
            GROUP BY demo.create_uid
        );
        """
        self.env.cr.execute(query)
