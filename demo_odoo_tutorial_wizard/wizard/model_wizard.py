from odoo import api, fields, models
from odoo.tools.misc import clean_context
import logging

_logger = logging.getLogger(__name__)

class DemoWizard(models.TransientModel):
    _name = "demo.wizard"
    _description = "Demo Wizard"

    wizard_partner_id = fields.Many2one('res.partner', string='Partner')
    wizard_test_context = fields.Char('wizard_test_context')

    @api.model
    def default_get(self, fields):
        res = super(DemoWizard, self).default_get(fields)
        context = clean_context(self.env.context) # pass "default_"
        if partner_id := context.get('partner_id'):
            res.update({
                'wizard_partner_id': partner_id,
            })
            # or
            # res['wizard_partner_id'] = partner_id
        return res

    def _dirty_check(self):
        _logger.warning('_dirty_check function')

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        """
        Overrides orm field_view_get.
        @return: Dictionary of Fields, arch and toolbar.
        """

        res = super().get_view(view_id, view_type, **options)
        self._dirty_check()
        return res

    def btn_validate(self):
        self.ensure_one()
        context = clean_context(self.env.context) # pass "default_"
        test_pass_data = context.get('test_pass_data')

        _logger.warning('============= btn_validate ==================')
        _logger.warning('test_pass_data: %s', test_pass_data)
        _logger.warning('wizard_test_context: %s', self.wizard_test_context)

        _logger.warning('active_id: %s', context['active_id'])
        _logger.warning('active_ids: %s', context['active_ids'])

        return {'type': 'ir.actions.act_window_close'}