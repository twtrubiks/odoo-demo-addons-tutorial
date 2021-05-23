from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class DemoCompany(models.Model):
    _name = 'demo.company'
    _description = 'Demo Company'

    name = fields.Char('Description', required=True)

    property_account_receivable_id = fields.Many2one('account.account',
        company_dependent=True,
        string="Account Receivable",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]",
        required=True)

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.user.company_id)

    def action_get_default_account(self):
        default_account = self.env['ir.property'].with_context(force_company=self.company_id.id).get('property_account_receivable_id', 'demo.company')
        _logger.warning(default_account)
        _logger.warning(self.property_account_receivable_id)
        _logger.warning('============= HELLO ==================')
