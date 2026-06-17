# report_strategy.py

class IReportStrategy:
    """Interface for report generation strategies."""

    def generate(self, balance) -> str:
        """Generate a report string from the given balance."""
        raise NotImplementedError("Subclasses must implement generate method.")


class SimpleSummaryStrategy(IReportStrategy):
    """Generates a single-line net balance summary."""

    def generate(self, balance) -> str:
        return f"Net Balance: ${balance.get_balance()}"


class DetailedSummaryStrategy(IReportStrategy):
    """Generates a detailed breakdown of income, expenses, and net balance."""

    def generate(self, balance) -> str:
        return (
            f"---- Financial Summary ----\n"
            f"  Total Income:   ${balance.get_total_income()}\n"
            f"  Total Expenses: ${balance.get_total_expenses()}\n"
            f"  Net Balance:    ${balance.get_balance()}\n"
            f"---------------------------"
        )
