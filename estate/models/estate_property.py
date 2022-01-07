from dateutil.relativedelta import relativedelta
from dateutil.utils import today
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property model"
    _order = "id desc"

    name = fields.Char(required=True, string="Title")
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
    minimum_acceptable = fields.Float()
    offer_price = fields.Float()

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)",
         "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)",
         "The selling price must be positive")
    ]

    # total_area compute function
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # best_price compute function
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            #if record:
                #record.best_price = max(record.offer_ids.mapped("price"))
            pass

    # garden onchange
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = ""
            self.garden_orientation = ""

    def real_estate_sold(self):
        if self.state == "Canceled":
            raise UserError("A canceled property cannot be sold")
        for record in self:
            record.state = "Sold"
        return True

    def real_estate_cancel(self):
        if self.state == "Sold":
            raise UserError("A sold property cannot be canceled")
        for record in self:
            record.state = "Canceled"
        return True

    #@api.constrains("expected_price", "offer_ids")
    #def _check_date_end(self):
        #for record in self:
            #record.offer_price = self.offer_ids.mapped("price")
            #record.minimum_acceptable = float(self.expected_price/100)*90
            #if float_compare(record.offer_price, record.minimum_acceptable) >= -1:
                #raise ValidationError("Offer price must be at least 90% of the expected price")
