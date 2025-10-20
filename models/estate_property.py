from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    # --- Defaults ---
    @api.model
    def _default_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    # --- Basic ---
    active = fields.Boolean(default=True)
    name = fields.Char(string="Title", required=True)
    price = fields.Float()

    # --- Status ---
    state = fields.Selection(
        [("new", "New"),
         ("offer", "Offer Received"),
         ("accepted", "Offer Accepted"),
         ("sold", "Sold"),
         ("canceled", "Canceled")],
        required=True, copy=False, default="new"
    )

    # --- Info umum ---
    postcode = fields.Char()
    date_availability = fields.Date(default=_default_availability, copy=False)
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    description = fields.Text()

    # --- Detail properti ---
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garden = fields.Boolean()
    garage = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        default="north"
    )
    total_area = fields.Integer(compute="_compute_total_area", store=True)

    # --- Relasi ---
    property_type_id = fields.Many2one("estate.property.type", string="Property Type",
                                       ondelete="set null", index=True, copy=False)
    buyer_id = fields.Many2one("res.partner", string="Buyer", ondelete="set null", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson",
                                     default=lambda self: self.env.user, ondelete="set null")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    best_offer = fields.Float(compute="_compute_best_offer")

    # --- Compute ---
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped("price")) if property.offer_ids else 0.0

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = (property.living_area or 0) + (property.garden_area or 0)

    # --- Onchange (Chapter 9) ---
    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                # set default values when checked
                property.garden_area = property.garden_area or 10
                property.garden_orientation = property.garden_orientation or "north"
            else:
                # clear when unchecked
                property.garden_area = 0
                property.garden_orientation = False

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        for property in self:
            if property.date_availability and property.date_availability < fields.Date.context_today(self):
                return {
                    "warning": {
                        "title": _("Warning"),
                        "message": _("Availability date is in the past."),
                    }
                }

    # --- Header Buttons (Chapter 10) ---
    def action_cancel(self):
        for property in self:
            if property.state == "sold":
                raise UserError(_("A sold property cannot be canceled."))
            property.state = "canceled"
        return True # Ditambahkan agar best practice

    def action_sold(self):
        for property in self:
            if property.state == "canceled":
                raise UserError(_("A canceled property cannot be sold."))
            property.state = "sold"
        return True # Ditambahkan agar best practice
    
    # --- Python Constraints (Chapter 11) ---
    @api.constrains("selling_price")
    def _check_constraint(self):
        for estate in self:
            if estate.selling_price < 5000:
                raise ValidationError(_("Test Manager"))

    # --- Delete Constraint (Chapter 12) ---
    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_not_new_or_canceled(self):
        if any(prop.state not in ('new', 'canceled') for prop in self):
            raise UserError(_("Only new or canceled properties can be deleted."))

