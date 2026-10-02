Adds numbered installment control to Odoo subscriptions (``sale_subscription``).

For every subscription you can set a maximum number of installments. Each
invoice generated from it (manually or by the recurring invoicing cron)
gets a legend such as "Billed installment 3 of 12" appended to every
product line, and once the last installment is confirmed the subscription
is closed automatically with the "End of contract" close reason.

The installment counter only moves forward when an invoice is confirmed,
so a draft invoice that is deleted or cancelled (for example, after a
failed automatic payment) never consumes an installment, and resetting a
confirmed invoice to draft and confirming it again does not skip one.
