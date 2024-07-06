from odoo import models, fields, api, Command
from odoo.exceptions import UserError

class DemoTag(models.Model):
    _name = 'demo.tag'
    _description = 'Demo Tags'
    _rec_name = 'complete_name'

    name = fields.Char(string='Tag Name', index=True, required=True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name')
    active = fields.Boolean(default=True, help="Set active.")

    @api.depends('name')
    def _compute_complete_name(self):
        for record in self:
            record.complete_name = f'hello world - {record.name}'

class DemoExpenseTutorial(models.Model):
    _name = 'demo.expense.tutorial'
    _description = 'Demo Expense Tutorial'
    _order = "sequence, id desc"
    _inherit = "analytic.mixin"

    name = fields.Char('Description', required=True)
    employee_id = fields.Many2one(
        'hr.employee',
        domain="[('user_id', '=', user_id)]",
        string="Employee", required=True)

    user_id = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user)

    # https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#relational-fields
    # Many2many(comodel_name=<object object>, relation=<object object>, column1=<object object>, column2=<object object>, string=<object object>, **kwargs)
    #
    # relation: database table name
    #

    # By default, the relationship table name is the two table names
    # joined with an underscore and _rel appended at the end.
    # In the case of our books or authors relationship, it should be named demo_expense_tutorial_demo_tag_rel.

    tag_ids = fields.Many2many('demo.tag', 'demo_expense_tag', 'demo_expense_id', 'tag_id',
        string='Tges', copy=False,
        groups='demo_expense_tutorial_v1.demo_expense_tutorial_group_manager'
    )
    sheet_id = fields.Many2one('demo.expense.sheet.tutorial', string="Expense Report", ondelete='restrict')
    sequence = fields.Integer(index=True, help="Gives the sequence order", default=1)
    active = fields.Boolean(default=True, help="Set active.")
    debug_field = fields.Char('debug_field')
    admin_field = fields.Char('admin_field')
    selet_fields = fields.Selection(
        selection='_selection_selet_fields'
    )
    analytic_distribution = fields.Json()
    # properties_definition_field = fields.PropertiesDefinition('properties_definition_field')

    resource_ref = fields.Reference(
        string='Record', selection='_selection_target_model')

    company_id_precompute = fields.Many2one(
        comodel_name='res.company',
        string="company",
        compute='_compute_company_id',
        store=True, precompute=True
    )
    """
    說明 precompute=True
    source code

    class Field(MetaField('DummyField', (object,), {})):

    precompute  need store true

    Odoo16: Add precompute=True option in your Computed fields to compute value before Record Create,
    UpTo 15.0 version Computed field value was computed after Record Create.

    https://github.com/odoo/odoo/commit/d04a5b5c8c7dc13e4e911a29d1944e90587e2883

    precompute    precompute
    False           True
    new              new
    new              new
    id               new


    建議使用 log_level = debug_sql 觀看過程

    precompute True    compute -> insert

    precompute False   insert -> compute -> update
    """

    data_vals = fields.Binary(compute='_compute_data_vals', exportable=False)

    @api.depends('employee_id')
    def _compute_company_id(self):
        for rec in self:
            rec.company_id_precompute = None

    @api.depends('name')
    def _compute_data_vals(self):
        for rec in self:
            rec.data_vals = {"tmp_data": "hello"}

    def custom_query(self):
        query = self._search([])
        query.add_where('1 = %s', [1,])
        query_string, query_param = query.select()
        self._cr.execute(query_string, query_param)
        # query.get_sql()
        pass

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] += '_trigger'
        return super().create(vals_list)

    # def write(self, vals):
    #     return super().write(vals)

    @api.model
    def _selection_target_model(self):
        return [(model.model, model.name) for model in self.env['ir.model'].sudo().search([])]

    def _selection_selet_fields(self):
        return [('a', '1'), ('b', '2')]

    def button_sheet_id(self):
        return {
            'view_mode': 'form',
            'res_model': 'demo.expense.sheet.tutorial',
            'res_id': self.sheet_id.id,
            'type': 'ir.actions.act_window'
        }

    def btn_test_acid_atomicity(self):
        # 不會建立資料, 也不會執行 done
        for index in range(3):
            self.create({
                'name': str(index),
                'employee_id': 1
            })
            if index == 1:
                raise UserError('error - auto rollback')
        print("done")

    def btn_test_savepoint_1(self):
        # 會建立資料 0_trigger 1_trigger, 會執行 done
        try:
            for index in range(3):
                self.create({
                    'name': str(index),
                    'employee_id': 1
                })
                if index == 1:
                    raise UserError('error - auto rollback')
        except Exception:
            pass
        print("done")

    def btn_test_savepoint_2(self):
        # 不會建立資料, 會執行 done
        # 可参考
        # https://github.com/odoo/odoo/issues/51331
        try:
            with self.env.cr.savepoint():
                for index in range(3):
                    self.create({
                        'name': str(index),
                        'employee_id': 1
                    })
                    if index == 1:
                        raise UserError('error - auto rollback')
        except Exception:
            pass
        print("done")

    def btn_test_savepoint_3(self):
        # 不會建立資料, 會執行 done
        try:
            for index in range(3):
                self.create({
                    'name': str(index),
                    'employee_id': 1
                })
                if index == 1:
                    raise UserError('error - auto rollback')
            # self.env.cr.commit()
        except Exception:
            self.env.cr.rollback()
        print("done")

    def btn_test_savepoint_4(self):
        # 會建立資料, 0_trigger 1_trigger 2_trigger, 會執行 done
        for index in range(3):
            try:
                self.create({
                    'name': str(index),
                    'employee_id': 1
                })
                if index == 1:
                    raise UserError('error - auto rollback')
            except Exception:
                pass
        print("done")

    def btn_test_savepoint_5(self):
        # 會建立資料 0_trigger 2_trigger
        for index in range(3):
            try:
                with self.env.cr.savepoint():
                    self.create({
                        'name': str(index),
                        'employee_id': 1
                    })
                    if index == 1:
                        raise UserError('error - auto rollback')
                    # self.env.cr.commit()
            except Exception:
                # self.env.cr.rollback()
                pass
        print("done")

    def btn_test_savepoint_6(self):
        # 會建立資料 0_trigger
        for index in range(3):
            try:
                with self.env.cr.savepoint():
                    self.create({
                        'name': str(index),
                        'employee_id': 1
                    })
                    if index == 1:
                        raise UserError('error - auto rollback')
                    self.env.cr.commit()
            except Exception:
                pass
        print("done")

    def btn_test_savepoint_7(self):
        # 會建立資料 2_trigger 3_trigger
        for index in range(4):
            try:
                with self.env.cr.savepoint():
                    self.create({
                        'name': str(index),
                        'employee_id': 1
                    })
                    if index == 1:
                        raise UserError('error - auto rollback')
            except Exception:
                self.env.cr.rollback()
        print("done")

    def btn_test_savepoint_8(self):
        # 會建立資料 2_trigger 3_trigger
        for index in range(4):
            try:
                self.create({
                    'name': str(index),
                    'employee_id': 1
                })
                if index == 1:
                    raise UserError('error - auto rollback')
            except Exception:
                self.env.cr.rollback()
        print("done")

    def btn_test_savepoint_9(self):
        # 會建立資料 0_trigger 2_trigger 3_trigger
        for index in range(4):
            try:
                self.create({
                    'name': str(index),
                    'employee_id': 1
                })
                if index == 1:
                    raise UserError('error - auto rollback')
                self.env.cr.commit()
            except Exception:
                self.env.cr.rollback()
        print("done")

    # @api.onchange('user_id')
    # def onchange_user_id(self):
    #     """
    #     https://github.com/odoo/odoo/pull/41918#issuecomment-824946980

    #     WARNING odoo.models:
    #     onchange method DemoExpenseTutorial.onchange_user_id returned a domain, this is deprecated
    #     """
    #     # domain
    #     result = dict()
    #     result['domain'] = {
    #         'employee_id': [('user_id', '=', self.user_id.id)]
    #     }
    #     return result

    @api.onchange('name')
    def onchange_name_warning(self):
        # warning message
        if self.name == 'test':
            result = dict()
            result['warning'] = {
                'title': 'HELLO',
                'message': 'I am warning'
            }
            return result


class DemoExpenseSheetTutorial(models.Model):
    _name = 'demo.expense.sheet.tutorial'
    _description = 'Demo Expense Sheet Tutorial'

    name = fields.Char('Expense Demo Report Summary', required=True)

    # One2many is a virtual relationship, there must be a Many2one field in the other_model,
    # and its name must be related_field
    expense_line_ids = fields.One2many(
        'demo.expense.tutorial', # related model
        'sheet_id', # field for "this" on related model
        string='Expense Lines')

    demo_expenses_count = fields.Integer(
        compute='_compute_demo_expenses_count',
        string='Demo Expenses Count')

    def add_demo_expense_record_old(self):
        # (0, _ , {'field': value}) creates a new record and links it to this one.

        data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')

        tag_data_1 = self.env.ref('demo_expense_tutorial_v1.demo_tag_data_1')
        tag_data_2 = self.env.ref('demo_expense_tutorial_v1.demo_tag_data_2')

        for record in self:
            # creates a new record
            val = {
                'name': 'test_data',
                'employee_id': data_1.employee_id,
                'tag_ids': [(6, 0, [tag_data_1.id, tag_data_2.id])]
            }

            self.expense_line_ids = [(0, 0, val)]

    def add_demo_expense_record(self):
        data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')

        tag_data_1 = self.env.ref('demo_expense_tutorial_v1.demo_tag_data_1')
        tag_data_2 = self.env.ref('demo_expense_tutorial_v1.demo_tag_data_2')

        for _ in self:
            val = {
                'name': 'test_data',
                'employee_id': data_1.employee_id.id,
                'tag_ids': [Command.set([tag_data_1.id, tag_data_2.id])]
            }
            self.expense_line_ids = [Command.create(val)]

    def link_demo_expense_record_old(self):
        # (4, id, _) links an already existing record.

        data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')

        for record in self:
            # link already existing record
            self.expense_line_ids = [(4, data_1.id, 0)]

    def link_demo_expense_record(self):
        data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')

        for _ in self:
            # link already existing record
            self.expense_line_ids = [Command.link(data_1.id)]

    def replace_demo_expense_record_old(self):
        # (6, _, [ids]) replaces the list of linked records with the provided list.

        data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')
        data_2 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_2')

        for record in self:
            # replace multi record
            self.expense_line_ids = [(6, 0, [data_1.id, data_2.id])]

    def replace_demo_expense_record(self):
        data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')
        data_2 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_2')

        for _ in self:
            # replace multi record
            self.expense_line_ids = [Command.set([data_1.id, data_2.id])]

    def clear_demo_expense_record(self):
        for _ in self:
            self.expense_line_ids = [Command.clear()]

    def button_line_ids(self):
        return {
            'name': 'Demo Expense Line IDs',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'demo.expense.tutorial',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('sheet_id', '=', self.id)],
        }

    def _compute_demo_expenses_count(self):
        # usually used read_group
        for record in self:
            record.demo_expenses_count = len(self.expense_line_ids)

    def name_get(self):
        names = []
        for record in self:
            name = f'{record.create_date.date()}-{record.name}'
            names.append((record.id, name))
        return names

    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        domain = domain or []
        if name:
            domain = domain + ['|', ('id', operator, name), ('name', operator, name)]
        return self._search(domain, limit=limit, order=order)
