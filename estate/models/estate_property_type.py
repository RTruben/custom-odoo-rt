from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type model"

    name = fields.Char(required=True)
