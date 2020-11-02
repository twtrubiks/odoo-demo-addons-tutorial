from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class DemoActionsSingleton(models.Model):
    _name = 'demo.actions.singleton'
    _description = 'Demo Actions Singleton'

    name = fields.Char('Description', required=True)

    def action_demo(self):
        self.ensure_one()
        _logger.warning('=== CALL action_demo ===')
