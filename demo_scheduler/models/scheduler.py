from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class DemoScheduler(models.Model):
    _name = 'demo.scheduler'
    _description = 'Demo Scheduler'

    def action_schedule(self):
        _logger.warning('============= Action Schedule ==================')
