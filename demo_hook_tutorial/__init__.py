from odoo import api, SUPERUSER_ID

import logging

_logger = logging.getLogger(__name__)

def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # data = env[......].search([......])

    _logger.warning('=== pre_init_hook ===')

def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # data = env[......].search([......])

    _logger.warning('=== post_init_hook ===')

def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # data = env[......].search([......])

    _logger.warning('=== uninstall_hook ===')

def post_load_hook():
    _logger.warning('=== post_load_hook ===')