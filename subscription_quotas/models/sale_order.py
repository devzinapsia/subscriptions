from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    next_quota = fields.Integer(
        string="Next installment",
        default=1,
        help="Installment number the next invoice will carry. It moves forward "
             "when an invoice carrying an installment is confirmed.",
    )
    max_quotas = fields.Integer(
        string="Maximum number of installments",
        default=0,
        help="Total number of installments of this subscription. Leave it at 0 "
             "to disable installment control. Once the last installment is "
             "invoiced and confirmed, the subscription is closed automatically.",
    )
    quota_legend = fields.Char(
        string="Line legend",
        default=lambda self: _("Billed installment %d of %d"),
        help="Text appended to every product line of the invoice. It must contain "
             "exactly two %d placeholders: the installment number and the total "
             "number of installments.",
    )

    @api.model
    def _quota_legend_is_valid(self, legend):
        if not legend or legend.count('%d') != 2:
            return False
        try:
            legend % (1, 1)
        except (TypeError, ValueError):
            return False
        return True

    @api.constrains('next_quota', 'max_quotas', 'quota_legend')
    def _check_quotas(self):
        for order in self:
            if order.max_quotas < 0:
                raise ValidationError(_("The maximum number of installments cannot be negative."))
            if not order.max_quotas:
                continue
            if order.next_quota < 1:
                raise ValidationError(_("The next installment must be 1 or greater."))
            if order.next_quota > order.max_quotas + 1:
                raise ValidationError(_(
                    "The next installment (%(next)s) cannot be greater than the maximum "
                    "number of installments plus one (%(max)s).",
                    next=order.next_quota, max=order.max_quotas + 1,
                ))
            if not self._quota_legend_is_valid(order.quota_legend):
                raise ValidationError(_(
                    "The line legend must contain exactly two %d placeholders "
                    "(installment number and total), e.g. \"Installment %d of %d\"."
                ))

    def _uses_quotas(self):
        self.ensure_one()
        return bool(
            self.is_subscription
            and self.max_quotas > 0
            and 1 <= self.next_quota <= self.max_quotas
            and self._quota_legend_is_valid(self.quota_legend)
        )

    def _create_invoices(self, grouped=False, final=False, date=None):
        """Append the installment legend to the new invoice lines.

        The installment counter is not moved here: it only moves forward when
        the invoice is confirmed (see account.move._post), so a draft invoice
        that gets deleted or cancelled (e.g. a failed automatic payment) does
        not consume an installment.
        """
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)

        for order in self:
            if not order._uses_quotas():
                continue

            legend = order.quota_legend % (order.next_quota, order.max_quotas)
            order_moves = moves.filtered(lambda m: m.invoice_origin == order.name)
            for line in order_moves.invoice_line_ids.filtered('product_id'):
                line.write({
                    'name': f"{line.name}\n{legend}",
                    'subscription_quota': order.next_quota,
                })

        return moves

    def _quota_register_invoiced(self, quota):
        """Move the counter past an invoiced installment, closing the
        subscription once its last installment has been invoiced.

        Uses max() so confirming the same invoice twice (reset to draft and
        confirm again) does not skip an installment.
        """
        end_of_contract = self.env.ref('sale_subscription.close_reason_end_of_contract')
        for order in self:
            order.next_quota = max(order.next_quota, quota + 1)
            if (
                order.max_quotas
                and order.next_quota > order.max_quotas
                and order.subscription_state in ('3_progress', '4_paused')
            ):
                order.set_close(close_reason_id=end_of_contract.id)
                order.message_post(body=_(
                    "Subscription closed automatically: all %(count)s installments have been invoiced.",
                    count=order.max_quotas,
                ))
