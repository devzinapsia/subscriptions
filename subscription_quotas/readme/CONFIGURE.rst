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
