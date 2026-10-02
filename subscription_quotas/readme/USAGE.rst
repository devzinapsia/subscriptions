#. Go to **Subscriptions** and open (or create) a subscription.
#. Set **Maximum number of installments**, and optionally adjust **Next
   installment** and **Line legend**.
#. Confirm the subscription and invoice it as usual, either manually or
   through the recurring invoicing cron.
#. Every product line of the invoice gets the legend, e.g. "Billed
   installment 1 of 12". When the invoice is confirmed, **Next installment**
   moves to the following number.
#. When the invoice carrying the last installment is confirmed, the
   subscription is closed automatically (close reason "End of contract")
   and a message is posted in its chatter.

Validation rules (only when a maximum is set):

* The maximum number of installments cannot be negative.
* The next installment must be between ``1`` and the maximum plus one.
* The line legend must contain exactly two ``%d`` placeholders.
