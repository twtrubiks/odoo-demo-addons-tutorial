from odoo import models, fields, api

class SaleOrderBarcodes(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "barcodes.barcode_events_mixin"]

    _barcode_scanned = fields.Char(string='Barcode', help="Here you can provide the barcode for the product")

    def on_barcode_scanned(self, barcode):
        product_obj = self.env['product.product'].search([('barcode', '=', barcode)], limit=1)
        val = {
            'product_id': product_obj,
            'product_uom_qty': 1,
            'price_unit': product_obj.lst_price
        }
        self.order_line = [(0, 0, val)]