from dateutil.utils import today

from odoo import api, models, fields
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[("Accepted", "Accepted"), ("Refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Datetime(compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)",
         "The offer price must be strictly positive")
    ]

    @api.depends("create_date", "validity", "date_deadline")
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = today() + relativedelta(days=record.validity)
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def real_estate_accept(self):
        for record in self:
            record.status = "Accepted"
        return True

    def real_estate_refuse(self):
        for record in self:
            record.status = "Refused"
        return True
