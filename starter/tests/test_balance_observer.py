import unittest
from io import StringIO
from unittest.mock import patch
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver, IBalanceObserver


class TestIBalanceObserver(unittest.TestCase):
    """Tests for the IBalanceObserver interface."""
    def test_base_class_raises_not_implemented(self):
        observer = IBalanceObserver()
        with self.assertRaises(NotImplementedError):
            observer.update(100, None)


class TestPrintObserver(unittest.TestCase):
    """Tests for the PrintObserver implementation of IBalanceObserver."""
    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.observer = PrintObserver()
        self.balance.register_observer(self.observer)

    def _apply_and_capture(self, transaction):
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            self.balance.apply_transaction(transaction)
            return mock_out.getvalue()

    def test_print_observer_outputs_correct_info(self):
        cases = [
            (Transaction(100, TransactionCategory.INCOME), "100"),
            (Transaction(50, TransactionCategory.EXPENSE), "Expense"),
        ]
        for transaction, expected in cases:
            with self.subTest(transaction=transaction):
                output = self._apply_and_capture(transaction)
                self.assertIn(expected, output)


class TestLowBalanceAlertObserver(unittest.TestCase):
    """Tests for the LowBalanceAlertObserver implementation of IBalanceObserver."""
    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered)

        self.balance.apply_transaction(Transaction(60, TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered)

    def test_alert_not_triggered_above_threshold(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)
        self.balance.apply_transaction(Transaction(200, TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered)

    def test_multiple_observers_all_notified(self):
        observer1 = LowBalanceAlertObserver(threshold=50)
        observer2 = LowBalanceAlertObserver(threshold=200)
        self.balance.register_observer(observer1)
        self.balance.register_observer(observer2)
        self.balance.apply_transaction(Transaction(100, TransactionCategory.INCOME))
        self.assertFalse(observer1.alert_triggered)
        self.assertTrue(observer2.alert_triggered)


if __name__ == "__main__":
    unittest.main()
