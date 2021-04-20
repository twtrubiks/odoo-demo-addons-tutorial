import json
from odoo import api, exceptions, fields, models, _
from lxml import etree
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountInvoice, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        print('view_type:', view_type)

        if not self.env.user.has_group('account.group_account_manager'):
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//field[@name="invoice_line_ids"]'):
                    print('node.attrib dict:', node.attrib)
                    node_values = node.get('modifiers')
                    modifiers = json.loads(node_values)
                    modifiers['readonly'] = True
                    node.set('modifiers', json.dumps(modifiers))
                res['arch'] = etree.tostring(doc)

        if self.env.user.has_group('account.group_account_manager'):
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//field[@name="partner_id"]'):
                    node.addnext(
                        etree.Element('field', {'string': 'test partner_id fields',
                                                'name': 'partner_id'}))
                res['arch'] = etree.tostring(doc)

        return res


