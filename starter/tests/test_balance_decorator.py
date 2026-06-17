# test_balance_decorator.py

import unittest
from io import StringIO
from unittest.mock import patch
from balance.balance import Balance
from balance.balance_decorator import (
    IBalanceDecorator,
    LoggingDecorator,
    ValidationDecorator,
)
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestIBalanceDecorator(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.decorator = IBalanceDecorator(self.balance)

    def test_delegates_apply_transaction(self):
        t = Transaction(100, TransactionCategory.INCOME)
        self.decorator.apply_transaction(t)
        self.assertEqual(self.decorator.get_balance(), 100)

    def test_delegates_get_balance(self):
        self.balance.add_income(200)
        self.assertEqual(self.decorator.get_balance(), 200)

    def test_delegates_get_total_income(self):
        self.balance.add_income(150)
        self.assertEqual(self.decorator.get_total_income(), 150)

    def test_delegates_get_total_expenses(self):
        self.balance.add_expense(50)
        self.assertEqual(self.decorator.get_total_expenses(), 50)

    def test_delegates_summary(self):
        result = self.decorator.summary()
        self.assertIn("Net Balance", result)


class TestLoggingDecorator(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.decorator = LoggingDecorator(self.balance)

    def test_applies_transaction(self):
        t = Transaction(100, TransactionCategory.INCOME)
        self.decorator.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_logs_before_transaction(self):
        t = Transaction(100, TransactionCategory.INCOME)
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            self.decorator.apply_transaction(t)
            output = mock_out.getvalue()
        self.assertIn("[LOG]", output)
        self.assertIn("Balance before", output)

    def test_logs_after_transaction(self):
        t = Transaction(100, TransactionCategory.INCOME)
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            self.decorator.apply_transaction(t)
            output = mock_out.getvalue()
        self.assertIn("Balance after", output)

    def test_logs_transaction_amount(self):
        t = Transaction(250, TransactionCategory.EXPENSE)
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            self.decorator.apply_transaction(t)
            output = mock_out.getvalue()
        self.assertIn("250", output)


class TestValidationDecorator(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.decorator = ValidationDecorator(self.balance)

    def test_valid_transaction_is_applied(self):
        t = Transaction(100, TransactionCategory.INCOME)
        self.decorator.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_zero_amount_raises_value_error(self):
        t = Transaction(0, TransactionCategory.INCOME)
        with self.assertRaises(ValueError):
            self.decorator.apply_transaction(t)

    def test_negative_amount_raises_value_error(self):
        t = Transaction(-50, TransactionCategory.EXPENSE)
        with self.assertRaises(ValueError):
            self.decorator.apply_transaction(t)

    def test_invalid_transaction_does_not_change_balance(self):
        t = Transaction(-100, TransactionCategory.INCOME)
        try:
            self.decorator.apply_transaction(t)
        except ValueError:
            pass
        self.assertEqual(self.balance.get_balance(), 0.0)


class TestStackedDecorators(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.decorated = LoggingDecorator(ValidationDecorator(self.balance))

    def test_valid_transaction_applied_through_stack(self):
        t = Transaction(300, TransactionCategory.INCOME)
        self.decorated.apply_transaction(t)
        self.assertEqual(self.balance.get_balance(), 300)

    def test_invalid_transaction_rejected_through_stack(self):
        t = Transaction(-100, TransactionCategory.INCOME)
        with self.assertRaises(ValueError):
            self.decorated.apply_transaction(t)

    def test_stacked_logging_still_outputs(self):
        t = Transaction(100, TransactionCategory.INCOME)
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            self.decorated.apply_transaction(t)
            output = mock_out.getvalue()
        self.assertIn("[LOG]", output)


if __name__ == "__main__":
    unittest.main()
