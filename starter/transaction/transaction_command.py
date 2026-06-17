# transaction_command.py

from balance.balance import Balance


class ITransactionCommand:
    """Interface for transaction commands."""

    def execute(self):
        """Apply the transaction to the balance."""
        raise NotImplementedError("Subclasses must implement execute().")

    def undo(self):
        """Reverse the transaction from the balance."""
        raise NotImplementedError("Subclasses must implement undo().")


class ApplyTransactionCommand(ITransactionCommand):
    """
    Command that applies a Transaction to the Balance.
    Supports undo by reversing the transaction effect.
    """

    def __init__(self, transaction):
        self.transaction = transaction
        self._balance = Balance.get_instance()

    def execute(self):
        """Apply the transaction to the balance."""
        self._balance.apply_transaction(self.transaction)

    def undo(self):
        """Reverse the transaction from the balance."""
        self._balance.reverse_transaction(self.transaction)
