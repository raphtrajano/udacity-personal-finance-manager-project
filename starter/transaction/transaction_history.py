# transaction_history.py


class TransactionHistory:
    """
    Manages undo/redo stacks for transaction commands.
    Acts as the invoker in the Command pattern.
    """

    def __init__(self):
        self._undo_stack = []
        self._redo_stack = []

    def execute(self, command):
        """Execute a command and push it onto the undo stack."""
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()

    def undo(self):
        """Undo the last executed command."""
        if not self._undo_stack:
            print("Nothing to undo.")
            return
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)
        print(f"Undid: {command.transaction}")

    def redo(self):
        """Redo the last undone command."""
        if not self._redo_stack:
            print("Nothing to redo.")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)
        print(f"Redid: {command.transaction}")

    def can_undo(self):
        """Return True if there is a command available to undo."""
        return bool(self._undo_stack)

    def can_redo(self):
        """Return True if there is a command available to redo."""
        return bool(self._redo_stack)
