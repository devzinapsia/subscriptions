# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    next_quota = fields.Integer(
        string="Próxima cuota", 
        default=1,
        help="Número de la cuota que se va a facturar."
    )
    max_quotas = fields.Integer(
        string="Cantidad máxima de cuotas", 
        default=1,
        help="Total de cuotas de la suscripción."
    )
    quota_legend = fields.Char(
        string="Leyenda artículo", 
        default="Cuota facturada %d de %d",
        help="Texto para la factura. Use %d para la cuota actual y el total."
    )

    def _create_recurring_invoice(self, batch_size=30):
        """
        Lógica mejorada: Solo interviene si existen cuotas definidas
        y la leyenda es válida.
        """
        # Ejecución estándar de Odoo
        invoices = super(SaleOrder, self)._create_recurring_invoice(batch_size=batch_size)
        
        for order in self:
            # 1. Validación de robustez: Si no es suscripción o los campos son 0/None, saltar.
            if not order.is_subscription:
                continue
            
            if not order.next_quota or not order.max_quotas:
                continue

            # 2. Verificar que la leyenda tenga exactamente los dos placeholders %d requeridos
            # Esto evita errores de "not enough arguments for format string"
            if not order.quota_legend or order.quota_legend.count('%d') < 2:
                continue

            # 3. Buscar facturas generadas para esta orden
            order_invoices = invoices.filtered(lambda i: i.invoice_origin == order.name)
            
            if order_invoices:
                for inv in order_invoices:
                    for line in inv.invoice_line_ids:
                        if not line.product_id:
                            continue
                            
                        try:
                            # Formateo seguro
                            formatted_legend = order.quota_legend % (order.next_quota, order.max_quotas)
                            line.name = f"{line.name}\n{formatted_legend}"
                        except (TypeError, ValueError):
                            # Si algo falla en el formateo a pesar de las validaciones, ignorar leyenda
                            continue
                
                # 4. Incremento de cuota solo si se procesó la factura
                order.next_quota += 1
                
        return invoices