from odoo import models, fields, tools
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class DemoCache(models.Model):
    _name = 'demo.cache'
    _description = 'demo cache'

    name = fields.Char('Description', required=True)

    @tools.ormcache()
    def demo_ormcache(self):
        result = '{} {}'.format('hello', 'world')
        _logger.warning(result)
        return result

    @tools.ormcache('self.env.uid')
    def demo_ormcache_by_env(self):
        result = '{} {} env uid'.format('hello', 'world')
        _logger.warning(result)
        return result

    @tools.ormcache_context(keys=('lang',))
    def demo_ormcache_context(self):
        result = '{} {} context'.format('hello', 'world')
        _logger.warning(result)
        return result

    def demo_clear_cache(self):
        # self.env[model_name].clear_caches()
        self.env['demo.cache'].clear_caches()
        raise ValidationError('clear cache')
