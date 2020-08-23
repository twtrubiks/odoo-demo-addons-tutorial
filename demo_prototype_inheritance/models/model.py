from odoo import models, fields, api

# prototype inheritance
class PrototypeInheritance(models.Model):
    _name = 'demo.prototype'
    _description = 'PrototypeInheritance'
    _inherit = ['mail.thread']

    # 'demo.prototype' 擁有 'mail.thread'(父類別) 的所有特性,
    # 在這裡面的修改, 都不會去影響到 'mail.thread'(父類別).

    test_field = fields.Char('test_field')