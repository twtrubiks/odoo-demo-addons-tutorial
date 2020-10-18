from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    demo_prefix = fields.Char(string="Demo Prefix")

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
