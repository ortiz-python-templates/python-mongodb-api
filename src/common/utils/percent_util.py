class PercentUtil:

    @staticmethod
    def percent_of(base: float, percent: float) -> float:
        """Calculates percent% of base."""
        return base * (percent / 100)

    @staticmethod
    def value_of(percent: float, amount: float) -> float:
        """Returns the base value given amount and percent%."""
        if percent == 0:
            raise ValueError("The percentage cannot be zero. Please provide a value greater than zero.")
        return amount * 100 / percent

    @staticmethod
    def increase_by_percent(amount: float, percent: float) -> float:
        """Increases amount by percent%."""
        return amount + PercentUtil.percent_of(amount, percent)

    @staticmethod
    def decrease_by_percent(amount: float, percent: float) -> float:
        """Decreases amount by percent%."""
        return amount - PercentUtil.percent_of(amount, percent)
