==================================
Control de cuotas de suscripciones
==================================

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

**Table of contents**

.. contents::
   :local:

Configuration
=============

Installment control is opt-in and configured per subscription. No global
configuration is required.

On a subscription, set **Maximum number of installments** to the total
number of installments of the plan. Leaving it at ``0`` (the default)
disables installment control for that subscription: no legend is added and
it is never closed automatically.

Once a maximum is set, two more fields are shown:

* **Next installment**: number the next invoice will carry. It starts at
  ``1``; set a higher value to start mid-plan (e.g. migrated contracts).
* **Line legend**: text appended to each invoice line. It must contain
  exactly two ``%d`` placeholders, the installment number and the total
  (e.g. ``Cuota %d de %d``). It defaults to "Billed installment %d of %d"
  in the user's language.

Usage
=====

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

Bug Tracker
===========

Bugs are tracked on
`GitHub Issues <https://github.com/devzinapsia/subscriptions/issues>`_.
In case of trouble, please check there if your issue has already been
reported.

Credits
=======

Authors
-------

* Zinapsia

Maintainers
-----------

This module is maintained by Zinapsia.

This module is part of the
`subscriptions <https://github.com/devzinapsia/subscriptions>`_
project.
