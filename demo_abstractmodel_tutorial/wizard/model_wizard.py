from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = "Report Wizard"

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)

    @api.multi
    def download_report(self):

        _logger.warning('=== CALL get_report ===')

        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
            },
        }
        return self.env.ref('demo_abstractmodel_tutorial.action_report_abstractmodel').report_action(self, data=data)

class ReportExpenseAbstractModel(models.AbstractModel):
    _name = 'report.demo_abstractmodel_tutorial.report_wizard_template'
    _description = 'Report Expense Wizard'

    @api.model
    def _get_report_values(self, docids, data=None):
        _logger.warning('=== CALL get_report_values ===')

        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        docs = self.env['hr.expense'].search([
            ('date', '>=', date_start),
            ('date', '<=', date_end)], order='date asc')
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }
