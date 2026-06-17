# test_transaction_command.py

import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_command import ITransactionCommand, ApplyTransactionCommand
from transaction.transaction_history import TransactionHistory


class TestITransactionCommand(unittest.TestCase):

    def test_execute_raises_not_implemented(self):
        cmd = ITransactionCommand()
        with self.assertRaises(NotImplementedError):
            cmd.execute()

    def test_undo_raises_not_implemented(self):
        cmd = ITransactionCommand()
        with self.assertRaises(NotImplementedError):
            cmd.undo()


class TestApplyTransactionCommand(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_execute_applies_income(self):
        t = Transaction(200, TransactionCategory.INCOME)
        cmd = ApplyTransactionCommand(t)
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), 200)

    def test_execute_applies_expense(self):
        t = Transaction(50, TransactionCategory.EXPENSE)
        cmd = ApplyTransactionCommand(t)
        cmd.execute()
        self.assertEqual(self.balance.get_balance(), -50)

    def test_undo_reverses_income(self):
        t = Transaction(200, TransactionCategory.INCOME)
        cmd = ApplyTransactionCommand(t)
        cmd.execute()
        cmd.undo()
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_undo_reverses_expense(self):
        self.balance.add_income(100)
        t = Transaction(40, TransactionCategory.EXPENSE)
        cmd = ApplyTransactionCommand(t)
        cmd.execute()
        cmd.undo()
        self.assertEqual(self.balance.get_balance(), 100)

    def test_undo_reverses_income_totals(self):
        t = Transaction(300, TransactionCategory.INCOME)
        cmd = ApplyTransactionCommand(t)
        cmd.execute()
        cmd.undo()
        self.assertEqual(self.balance.get_total_income(), 0.0)

    def test_undo_reverses_expense_totals(self):
        t = Transaction(80, TransactionCategory.EXPENSE)
        cmd = ApplyTransactionCommand(t)
        cmd.execute()
        cmd.undo()
        self.assertEqual(self.balance.get_total_expenses(), 0.0)


class TestTransactionHistory(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.history = TransactionHistory()

    def test_execute_applies_transaction(self):
        cmd = ApplyTransactionCommand(Transaction(100, TransactionCategory.INCOME))
        self.history.execute(cmd)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_undo_reverses_last_transaction(self):
        self.history.execute(ApplyTransactionCommand(Transaction(100, TransactionCategory.INCOME)))
        self.history.execute(ApplyTransactionCommand(Transaction(40, TransactionCategory.EXPENSE)))
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 100)

    def test_redo_reapplies_undone_transaction(self):
        self.history.execute(ApplyTransactionCommand(Transaction(100, TransactionCategory.INCOME)))
        self.history.execute(ApplyTransactionCommand(Transaction(40, TransactionCategory.EXPENSE)))
        self.history.undo()
        self.history.redo()
        self.assertEqual(self.balance.get_balance(), 60)

    def test_undo_clears_redo_stack_on_new_execute(self):
        self.history.execute(ApplyTransactionCommand(Transaction(100, TransactionCategory.INCOME)))
        self.history.undo()
        self.history.execute(ApplyTransactionCommand(Transaction(50, TransactionCategory.INCOME)))
        self.assertFalse(self.history.can_redo())

    def test_can_undo_false_when_empty(self):
        self.assertFalse(self.history.can_undo())

    def test_can_redo_false_when_empty(self):
        self.assertFalse(self.history.can_redo())

    def test_can_undo_true_after_execute(self):
        self.history.execute(ApplyTransactionCommand(Transaction(50, TransactionCategory.INCOME)))
        self.assertTrue(self.history.can_undo())

    def test_can_redo_true_after_undo(self):
        self.history.execute(ApplyTransactionCommand(Transaction(50, TransactionCategory.INCOME)))
        self.history.undo()
        self.assertTrue(self.history.can_redo())

    def test_multiple_undos(self):
        self.history.execute(ApplyTransactionCommand(Transaction(100, TransactionCategory.INCOME)))
        self.history.execute(ApplyTransactionCommand(Transaction(50, TransactionCategory.INCOME)))
        self.history.undo()
        self.history.undo()
        self.assertEqual(self.balance.get_balance(), 0.0)


if __name__ == "__main__":
    unittest.main()
