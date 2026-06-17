# transaction.py

from transaction.transaction_category import TransactionCategory
from transaction.transaction_type import TransactionType

class Transaction:
    """Represents a financial transaction with an amount and category."""

    def __init__(self, amount, category: TransactionCategory):
        self.amount = amount
        self.category = category
        self.type = TransactionType.INCOME if category == TransactionCategory.INCOME else TransactionType.EXPENSE

    # String representation for debugging and display.
    def __str__(self):
        return f"Transaction(${self.amount}, category='{self.category}')"

    # Equality check to compare transactions based on amount, category, and type.
    def __eq__(self, other):
        if not isinstance(other, Transaction):
            return NotImplemented
        return (self.amount == other.amount and
                self.category == other.category and
                self.type == other.type)
