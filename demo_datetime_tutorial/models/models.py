from odoo import models, fields, api
from pytz import timezone
import logging

_logger = logging.getLogger(__name__)

class DemoDatetime(models.Model):
    _name = "demo.datetime"
    _description = 'Demo Datetime Tutorial'

    name = fields.Char('Name', required=True)
    my_datetime = fields.Datetime(
        'my_datetime', default=fields.Datetime.now())

    def demo1(self):
        _logger.warning('db datetime')
        _logger.warning(self.my_datetime )

        _logger.warning('Asia/Taipei datetime')
        _logger.warning(self.my_datetime.astimezone(timezone('Asia/Taipei')))

