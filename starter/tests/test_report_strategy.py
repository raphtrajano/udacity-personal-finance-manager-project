import unittest
from balance.balance import Balance
from balance.report_strategy import IReportStrategy, SimpleSummaryStrategy, DetailedSummaryStrategy
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestIReportStrategy(unittest.TestCase):

    def test_base_class_raises_not_implemented(self):
        strategy = IReportStrategy()
        with self.assertRaises(NotImplementedError):
            strategy.generate(None)


class TestSimpleSummaryStrategy(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.strategy = SimpleSummaryStrategy()

    def test_simple_summary_format(self):
        self.balance.add_income(100)
        result = self.strategy.generate(self.balance)
        self.assertEqual(result, "Net Balance: $100.0")

    def test_simple_summary_zero_balance(self):
        result = self.strategy.generate(self.balance)
        self.assertEqual(result, "Net Balance: $0.0")

    def test_simple_summary_negative_balance(self):
        self.balance.add_expense(50)
        result = self.strategy.generate(self.balance)
        self.assertEqual(result, "Net Balance: $-50.0")


class TestDetailedSummaryStrategy(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.strategy = DetailedSummaryStrategy()

    def test_detailed_summary_contains_income(self):
        self.balance.add_income(300)
        result = self.strategy.generate(self.balance)
        self.assertIn("300", result)

    def test_detailed_summary_contains_expenses(self):
        self.balance.add_expense(100)
        result = self.strategy.generate(self.balance)
        self.assertIn("100", result)

    def test_detailed_summary_contains_net_balance(self):
        self.balance.add_income(500)
        self.balance.add_expense(200)
        result = self.strategy.generate(self.balance)
        self.assertIn("300", result)

    def test_detailed_summary_sections_present(self):
        result = self.strategy.generate(self.balance)
        self.assertIn("Total Income", result)
        self.assertIn("Total Expenses", result)
        self.assertIn("Net Balance", result)


class TestStrategySwapping(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.balance.apply_transaction(Transaction(500, TransactionCategory.INCOME))
        self.balance.apply_transaction(Transaction(100, TransactionCategory.EXPENSE))

    def test_default_strategy_is_simple(self):
        result = self.balance.summary()
        self.assertEqual(result, "Net Balance: $400.0")

    def test_swap_to_detailed_strategy(self):
        self.balance.set_report_strategy(DetailedSummaryStrategy())
        result = self.balance.summary()
        self.assertIn("Total Income", result)
        self.assertIn("Total Expenses", result)

    def test_swap_back_to_simple_strategy(self):
        self.balance.set_report_strategy(DetailedSummaryStrategy())
        self.balance.set_report_strategy(SimpleSummaryStrategy())
        result = self.balance.summary()
        self.assertEqual(result, "Net Balance: $400.0")


if __name__ == "__main__":
    unittest.main()
