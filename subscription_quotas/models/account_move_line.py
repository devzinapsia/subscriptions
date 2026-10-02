from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    subscription_quota = fields.Integer(
        string="Installment number",
        copy=False,
        readonly=True,
        help="Subscription installment this line invoices. The subscription "
             "counter only moves forward when the invoice is confirmed.",
    )
