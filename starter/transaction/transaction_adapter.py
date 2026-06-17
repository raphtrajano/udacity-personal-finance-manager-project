# transaction_adapter.py

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.external_income_transaction import ExternalFreelanceIncome

class TransactionAdapter:
    def __init__(self, external_transaction):
        self.external_transaction = external_transaction

    def to_transaction(self):
        """Convert an external income transaction to a standard Transaction."""
        category = TransactionCategory.INCOME if self.external_transaction.type == 'income' else TransactionCategory.EXPENSE
        return Transaction(self.external_transaction.amount, category)
