from odoo import models, fields, api

class DemoHierarchyTutorial(models.Model):
    _name = 'demo.hierarchy'
    _description = 'Demo Hierarchy Tutorial'

    name = fields.Char(string='name', index=True)
    parent_id = fields.Many2one('demo.hierarchy', string='Related Partner', index=True)
    parent_name = fields.Char(related='parent_id.name', readonly=True, string='Parent name')
    child_ids = fields.One2many('demo.hierarchy', 'parent_id', string='Contacts', domain=[('active', '=', True)])
    active = fields.Boolean(default=True)
