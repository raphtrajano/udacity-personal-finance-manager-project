# transaction_adapter.py

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TransactionAdapter:
    """Adapts an ExternalFreelanceIncome into a standard Transaction object."""

    def __init__(self, external_transaction):
        self.external_transaction = external_transaction

    def to_transaction(self):
        """Convert an external income transaction to a standard Transaction."""
        category = (
            TransactionCategory.INCOME
            if self.external_transaction.type == 'income'
            else TransactionCategory.EXPENSE
        )
        return Transaction(self.external_transaction.amount, category)
