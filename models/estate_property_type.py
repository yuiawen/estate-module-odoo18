from odoo import _, api, fields, models

class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _inherit = ["estate.mixin"]
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=1)
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("estate.property.offer", "type_id", string="Offers")
    offer_count = fields.Integer(string="Offers", compute="_compute_offer_count")
    property_count = fields.Integer(string="Properties", compute="_compute_property_count")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.name:
                self.env["estate.property.tag"].create({"name": rec.name})
        return records

    def unlink(self):
        for rec in self:
            if rec.property_ids:
                rec.property_ids.write({"property_type_id": False})
        return super().unlink()

    @api.depends("property_ids")
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    def action_open_property_ids(self):
        self.ensure_one()
        return {
            "name": _("Related Properties"),
            "type": "ir.actions.act_window",
            "res_model": "estate.property",
            "view_mode": "tree,form",
            "target": "current",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id},
        }
