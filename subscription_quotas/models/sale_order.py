# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    next_quota = fields.Integer(string="Próxima cuota", default=1)
    max_quotas = fields.Integer(string="Cantidad máxima de cuotas", default=1)
    quota_legend = fields.Char(string="Leyenda artículo", default="Cuota facturada %d de %d")

    def _create_invoices(self, grouped=False, final=False, date=None):
        """
        En Odoo 18, este es el método principal que crea facturas 
        desde una orden (incluyendo suscripciones).
        """
        moves = super(SaleOrder, self)._create_invoices(grouped=grouped, final=final, date=date)
        
        for order in self:
            # Validaciones de robustez
            if not order.is_subscription or not order.next_quota or not order.max_quotas:
                continue
            
            if not order.quota_legend or order.quota_legend.count('%d') < 2:
                continue

            # Buscamos las facturas recién creadas para esta orden
            order_moves = moves.filtered(lambda m: m.invoice_origin == order.name)
            
            if order_moves:
                for move in order_moves:
                    for line in move.invoice_line_ids:
                        if not line.product_id:
                            continue
                        
                        try:
                            # Generamos la leyenda: "Cuota 1 de 12"
                            legend = order.quota_legend % (order.next_quota, order.max_quotas)
                            # Actualizamos la descripción de la línea
                            line.name = f"{line.name}\n{legend}"
                        except:
                            continue
                
                # REQUERIMIENTO 4: Incrementar en uno la próxima cuota
                order.next_quota += 1
                
        return moves