from odoo import _, api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    def _create_demo_sequence(self):
        demo_vals = []
        for company in self:
            demo_vals.append({
                'name': f'demo_sequence_sequence - {company.name} company',
                'code': 'demo.sequence',
                'company_id': company.id,
                'prefix': '%(year)s%(month)s%(day)s',
                'padding': 5,
                'number_next': 1,
                'number_increment': 1
            })
        if demo_vals:
            self.env['ir.sequence'].create(demo_vals)

    @api.model
    def create_missing_demo_sequence_sequence(self):
        company_ids  = self.env['res.company'].search([])
        domain = [('code', '=', 'demo.sequence')]
        company_has_demo_seq = self.env['ir.sequence'].search(domain).mapped('company_id')
        company_todo_sequence = company_ids - company_has_demo_seq
        company_todo_sequence._create_demo_sequence()

    def _create_per_company_sequences(self):
        self.ensure_one()
        self._create_demo_sequence()

    @api.model_create_multi
    def create(self, vals_list):
        companies = super().create(vals_list)
        for company in companies:
            company.sudo()._create_per_company_sequences()

        # 如果有建立分公司要多建立的東西可以寫在這邊
        return companies
