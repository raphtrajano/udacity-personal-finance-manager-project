# balance_decorator.py


class IBalanceDecorator:
    """
    Base decorator interface that wraps a Balance instance.
    Subclasses can override apply_transaction() to add behaviour
    before/after delegating to the wrapped balance.
    """

    def __init__(self, balance):
        self._balance = balance

    def apply_transaction(self, transaction):
        """Delegate to the wrapped balance by default."""
        self._balance.apply_transaction(transaction)

    def get_balance(self):
        return self._balance.get_balance()

    def get_total_income(self):
        return self._balance.get_total_income()

    def get_total_expenses(self):
        return self._balance.get_total_expenses()

    def summary(self):
        return self._balance.summary()


class LoggingDecorator(IBalanceDecorator):
    """
    Decorator that logs each transaction before and after it is applied.
    """

    def apply_transaction(self, transaction):
        print(
            f"[LOG] Applying {transaction.type.value}: "
            f"${transaction.amount} | Balance before: ${self._balance.get_balance()}"
        )
        self._balance.apply_transaction(transaction)
        print(f"[LOG] Balance after: ${self._balance.get_balance()}")


class ValidationDecorator(IBalanceDecorator):
    """
    Decorator that validates a transaction before applying it.
    Rejects transactions with non-positive amounts.
    """

    def apply_transaction(self, transaction):
        if transaction.amount <= 0:
            raise ValueError(
                f"Invalid transaction: amount must be positive, "
                f"got ${transaction.amount}."
            )
        self._balance.apply_transaction(transaction)
