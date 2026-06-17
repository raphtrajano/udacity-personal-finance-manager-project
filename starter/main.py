"""This module serves as the entry point for the program."""
from balance.balance import Balance
from balance.balance_decorator import LoggingDecorator, ValidationDecorator
from balance.balance_observer import LowBalanceAlertObserver
from balance.balance_observer import PrintObserver
from balance.report_strategy import SimpleSummaryStrategy, DetailedSummaryStrategy
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_adapter import TransactionAdapter
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_command import ApplyTransactionCommand
from transaction.transaction_history import TransactionHistory


def main():
    print("Adding transactions...")

    # Create balance and add observers
    balance = Balance.get_instance()
    balance.reset()
    balance.register_observer(PrintObserver())
    balance.register_observer(LowBalanceAlertObserver(threshold=100))

    # Create standard transactions
    transactions = [
        Transaction(100, TransactionCategory.INCOME),
        Transaction(50, TransactionCategory.EXPENSE),
        Transaction(200, TransactionCategory.INCOME),
        Transaction(75, TransactionCategory.EXPENSE),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(1200, "INV-98765", "Mobile App Project")
    adapter = TransactionAdapter(freelance_income)
    adapted_transaction = adapter.to_transaction()

    all_transactions = transactions + [adapted_transaction]

    # Command pattern: apply all transactions via history
    history = TransactionHistory()
    for transaction in all_transactions:
        history.execute(ApplyTransactionCommand(transaction))

    # Decorator pattern: wrap balance with logging + validation
    decorated_balance = LoggingDecorator(ValidationDecorator(balance))
    print("\n----- Decorator pattern demo -----")
    decorated_balance.apply_transaction(Transaction(500, TransactionCategory.INCOME))

    # Strategy pattern: simple summary (default)
    balance.set_report_strategy(SimpleSummaryStrategy())
    print(balance.summary())

    # Command pattern: undo last transaction and show updated balance
    print("\n----- Undoing last transaction -----")
    history.undo()
    print(balance.summary())

    # Command pattern: redo the undone transaction
    print("\n----- Redoing last transaction -----")
    history.redo()
    print(balance.summary())

    # Strategy pattern: swap to detailed summary
    balance.set_report_strategy(DetailedSummaryStrategy())
    print(f"\n{balance.summary()}")


if __name__ == "__main__":
    main()
