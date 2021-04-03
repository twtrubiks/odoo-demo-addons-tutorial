from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    demo_prefix = fields.Char(
                string="Demo Prefix",
                # config_parameter='demo_config_settings.config.demo_prefix',
                )

    group_demo_config_setting = fields.Boolean("Demo Config",
        group='base.group_user', # default
        # group='demo_config_settings.demo_config_settings_tutorial_group',
        implied_group='sale.group_delivery_invoice_address',
        )

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        demo_prefix = self.env["ir.config_parameter"].get_param("demo_config_settings.config.demo_prefix", False)
        res.update({
            'demo_prefix': demo_prefix,
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('demo_config_settings.config.demo_prefix', self.demo_prefix)
