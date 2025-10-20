from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _inherit = "estate.mixin"
    _description = "Tags of Real Estate Model"

    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "Tag name should be unique"),
    ]
    _oder = "name desc"
    color = fields.Integer()