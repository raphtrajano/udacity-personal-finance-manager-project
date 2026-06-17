import unittest
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestTransactionAdapter(unittest.TestCase):

    def setUp(self):
        self.ext_txn = ExternalFreelanceIncome(500, "INV-12345", "Website development")
        self.adapter = TransactionAdapter(self.ext_txn)

    def test_adapter_converts_freelance_income(self):
        txn = self.adapter.to_transaction()
        self.assertEqual(txn, Transaction(500, TransactionCategory.INCOME))

    def test_adapter_preserves_amount(self):
        txn = self.adapter.to_transaction()
        self.assertEqual(txn.amount, 500)

    def test_adapter_always_returns_income_category(self):
        txn = self.adapter.to_transaction()
        self.assertEqual(txn.category, TransactionCategory.INCOME)

    def test_adapter_returns_transaction_instance(self):
        txn = self.adapter.to_transaction()
        self.assertIsInstance(txn, Transaction)

    def test_adapter_with_different_amounts(self):
        ext = ExternalFreelanceIncome(1200, "INV-99999", "Mobile App Project")
        txn = TransactionAdapter(ext).to_transaction()
        self.assertEqual(txn.amount, 1200)
        self.assertEqual(txn.category, TransactionCategory.INCOME)


if __name__ == "__main__":
    unittest.main()
