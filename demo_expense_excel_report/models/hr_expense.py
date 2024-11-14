from odoo import models, fields, api
import json
import xlsxwriter
import io

class HrExpenseCustom(models.Model):
    _inherit = "hr.expense"

    def button_excel_report(self):
        data = {
            'model_id': self.id,
            'name': self.name,
        }
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'hr.expense',
                'options': json.dumps(data),
                'output_format': 'xlsx',
                'report_name': 'Expense Custom Excel Report',
            },
            'report_type': 'xlsx',
        }


    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        sheet.write(0, 2, data['name'])
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
