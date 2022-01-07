from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag model"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ("uniq_name", "UNIQUE(name)", "The tag name must be unique")
    ]