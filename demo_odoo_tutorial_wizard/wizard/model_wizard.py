from odoo import api, fields, models
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
        default_partner_id = self.env.context.get('default_partner_id', [])
        res.update({
            'wizard_partner_id': default_partner_id,
        })
        # or
        # res['wizard_partner_id'] = default_partner_id
        return res

    def btn_validate(self):
        self.ensure_one()
        context = dict(self._context or {})
        default_test_pass_data = context.get('default_test_pass_data', [])

        _logger.warning('============= btn_validate ==================')
        _logger.warning('default_test_pass_data: %s', default_test_pass_data)
        _logger.warning('wizard_test_context: %s', self.wizard_test_context)

        return {'type': 'ir.actions.act_window_close'}