import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_type import TransactionType


class TestTransaction(unittest.TestCase):

    def test_transaction_creation(self):
        t = Transaction(100, TransactionCategory.EXPENSE)
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, TransactionCategory.EXPENSE)

    def test_transaction_str(self):
        t = Transaction(50, TransactionCategory.INCOME)
        self.assertEqual(str(t), "Transaction($50, category='TransactionCategory.INCOME')")

    def test_transaction_equality(self):
        t1 = Transaction(20, TransactionCategory.EXPENSE)
        t2 = Transaction(20, TransactionCategory.EXPENSE)
        t3 = Transaction(30, TransactionCategory.EXPENSE)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)

    def test_income_transaction_type(self):
        t = Transaction(100, TransactionCategory.INCOME)
        self.assertEqual(t.type, TransactionType.INCOME)

    def test_expense_transaction_type(self):
        t = Transaction(100, TransactionCategory.EXPENSE)
        self.assertEqual(t.type, TransactionType.EXPENSE)

    def test_inequality_different_category(self):
        t1 = Transaction(100, TransactionCategory.INCOME)
        t2 = Transaction(100, TransactionCategory.EXPENSE)
        self.assertNotEqual(t1, t2)

    def test_equality_with_non_transaction_returns_not_implemented(self):
        t = Transaction(100, TransactionCategory.INCOME)
        self.assertEqual(t.__eq__("not a transaction"), NotImplemented)


class TestTransactionType(unittest.TestCase):

    def test_income_enum_value(self):
        self.assertEqual(TransactionType.INCOME.value, "Income")

    def test_expense_enum_value(self):
        self.assertEqual(TransactionType.EXPENSE.value, "Expense")

    def test_enum_members_exist(self):
        self.assertIn(TransactionType.INCOME, TransactionType)
        self.assertIn(TransactionType.EXPENSE, TransactionType)


if __name__ == "__main__":
    unittest.main()
