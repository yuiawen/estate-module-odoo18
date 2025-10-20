from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    # ---- fields utama ----
    price = fields.Float(required=True)
    status = fields.Selection(
        [("new", "New"), ("accepted", "Accepted"), ("refused", "Refused")],
        required=True, default="new"
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True, ondelete="restrict")
    property_id = fields.Many2one("estate.property", string="Property", required=True, ondelete="cascade")
    type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    # ---- validity & deadline (harus di model offer) ----
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline",
                                inverse="_inverse_date_deadline",
                                store=True)

    # ---- compute/inverse ----
    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            base = (offer.create_date.date()
                    if offer.create_date
                    else fields.Date.context_today(self))
            offer.date_deadline = base + relativedelta(days=offer.validity or 0)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                base = (offer.create_date.date()
                        if offer.create_date
                        else fields.Date.context_today(self))
                offer.validity = (offer.date_deadline - base).days
            else:
                offer.validity = 0

    # --- Metode Tombol ---
    def action_accept(self):
        for offer in self:
            offer.status = "accepted"
            
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "accepted"

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"

