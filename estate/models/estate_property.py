from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    available_from = fields.Date(copy=False, default=today()+relativedelta(months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("North", "North"), ("South", "South"), ("East", "East"), ("West", "West")])
    active = fields.Boolean(default=True)
    state = fields.Selection(required=True, copy=False,
                             selection=[("New", "New"), ("Offer received", "Offer received"),
                                        ("Offer Accepted", "Offer Accepted"), ("Sold", "Sold"),
                                        ("Canceled", "Canceled")], default="New")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.uid)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Integer(compute="_compute_best_price")

    # total_area compute function
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # best_price compute function
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'))

    # garden onchange
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = ""
            self.garden_orientation = ""
