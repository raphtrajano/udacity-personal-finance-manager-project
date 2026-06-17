# balance_observer.py

class IBalanceObserver:
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message whenever the balance changes."""
        print(f"Balance updated: ${balance} (after {transaction.type.value} of ${transaction.amount})")


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        self.threshold = threshold
        self.alert_triggered = False

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        if balance < self.threshold:
            self.alert_triggered = True
            print(f"Alert: Low balance detected! Current balance is ${balance}, which is below the threshold of ${self.threshold}.")
        else:
            self.alert_triggered = False
