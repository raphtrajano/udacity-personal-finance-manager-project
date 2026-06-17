# balance.py

from transaction.transaction_category import TransactionCategory

class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __new__(cls):
        # Ensure only one instance of Balance exists.
        if cls._instance is None:
            print("No instance found, creating new one.")
            cls._instance = super(Balance, cls).__new__(cls)
            cls._instance._total_balance = 0.0
            cls._instance._observers = []
        return cls._instance

    def __init__(self):
        """Initialize the balance. Prevent direct instantiation."""
        pass

    @classmethod
    def get_instance(cls):
        """Get the singleton instance of Balance."""
        if cls._instance is None:
            cls()
        return cls._instance

    def reset(self):
        """Reset the net balance to zero and clear all observers."""
        self._total_balance = 0.0
        self._observers = []

    def register_observer(self, observer):
        """Register an observer to receive balance update notifications."""
        self._observers.append(observer)

    def notify_observers(self, transaction):
        """Notify all registered observers of a balance change."""
        for observer in self._observers:
            observer.update(self._total_balance, transaction)

    def add_income(self, amount):
        """Add income to the balance."""
        self._total_balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self._total_balance -= amount

    def apply_transaction(self, transaction):
        """
        Apply a Transaction object to update the balance and notify observers.

        Args:
            transaction (Transaction): The transaction to apply.
        """
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        else:
            raise ValueError(f"Unknown transaction category: {transaction.category}")
        self.notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._total_balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Net Balance: ${self._total_balance}"
    
