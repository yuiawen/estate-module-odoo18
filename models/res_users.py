from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    # relasi ke estate.property melalui salesperson_id
    property_ids = fields.One2many(
        "estate.property", "salesperson_id", string="Properties"
    )
