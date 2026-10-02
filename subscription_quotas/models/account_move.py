from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        posted = super()._post(soft=soft)
        for move in posted.filtered(lambda m: m.move_type == 'out_invoice'):
            for line in move.invoice_line_ids.filtered('subscription_quota'):
                orders = line.sale_line_ids.order_id.filtered('is_subscription')
                orders._quota_register_invoiced(line.subscription_quota)
        return posted
