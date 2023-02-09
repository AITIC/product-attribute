# Copyright 2015 ADHOC SA  (http://www.adhoc.com.ar)
# Copyright 2015-2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Define all the related fields in product.template with 'readonly=False'
    # to be able to modify the values from product.template.
    dimensional_uom_id = fields.Many2one(
        "uom.uom",
        "Dimensional UoM",
        related="product_variant_ids.dimensional_uom_id",
        help="UoM for length, height, width",
        readonly=False ,copy=True
    )
    product_length = fields.Float(
        related="product_variant_ids.product_length", readonly=False,copy=True
    )
    product_height = fields.Float(
        related="product_variant_ids.product_height", readonly=False,copy=True
    )
    product_width = fields.Float(
        related="product_variant_ids.product_width", readonly=False,copy=True
    )

    @api.model
    def _calc_volume(self, product_length, product_height, product_width, uom_id):
        volume = 0
        if product_length and product_height and product_width and uom_id:
            length_m = self.convert_to_meters(product_length, uom_id)
            height_m = self.convert_to_meters(product_height, uom_id)
            width_m = self.convert_to_meters(product_width, uom_id)
            volume = length_m * height_m * width_m

        return volume

    @api.onchange(
        "product_length", "product_height", "product_width", "dimensional_uom_id"
    )
    def onchange_calculate_volume(self):
        self.volume = self._calc_volume(
            self.product_length,
            self.product_height,
            self.product_width,
            self.dimensional_uom_id,
        )

    def convert_to_meters(self, measure, dimensional_uom):
        uom_meters = self.env.ref("uom.product_uom_meter")

        return dimensional_uom._compute_quantity(
            qty=measure,
            to_unit=uom_meters,
            round=False,
        )

    @api.model
    def create(self, vals):       
        ctx = dict(self._context)
        ctx.update({'default_dimensional_uom_id':vals['dimensional_uom_id'], 'default_product_width':vals['product_width'],'default_product_length':vals['product_length'],'default_product_height':vals['product_height']})         
        result = super(ProductTemplate, self.with_context(ctx)).create(vals)               
        return result

