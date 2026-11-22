"""Services sold by Software FJ. Each subclass prices itself differently."""

from abc import abstractmethod

from entity import Entity
from exceptions import (
    InconsistentCalculationError,
    InvalidReservationError,
    MissingParameterError,
    ServiceUnavailableError,
)


class Service(Entity):
    def __init__(self, identifier, name, base_rate, available=True):
        super().__init__(identifier, name)
        if base_rate is None:
            raise MissingParameterError("base rate is required")
        if base_rate < 0:
            raise InconsistentCalculationError(
                f"base rate for {name} cannot be negative"
            )
        self._base_rate = float(base_rate)
        self._available = bool(available)

    @property
    def base_rate(self):
        return self._base_rate

    @property
    def available(self):
        return self._available

    def validate(self, hours, discount=0.0, tax_rate=0.19):
        if hours is None:
            raise MissingParameterError("duration is required")
        if hours <= 0:
            raise InconsistentCalculationError("duration must be greater than zero")
        if discount < 0 or discount > 1:
            raise InconsistentCalculationError(
                "discount must be a fraction between 0 and 1"
            )
        if tax_rate < 0:
            raise InconsistentCalculationError("tax rate cannot be negative")
        if not self._available:
            raise ServiceUnavailableError(f"{self.name} is not available")

    def calculate_cost(self, hours, discount=0.0, tax_rate=0.19):
        """Full price. discount and tax_rate are optional."""
        self.validate(hours, discount, tax_rate)
        subtotal = self._raw_amount(hours)
        taxed = subtotal * (1 + tax_rate)
        return int(round(taxed * (1 - discount)))

    def calculate_cost_with_discount(self, hours, discount):
        """Price with a discount and no tax."""
        return self.calculate_cost(hours, discount=discount, tax_rate=0.0)

    def calculate_cost_with_tax(self, hours, tax_rate):
        """Price with tax and no discount."""
        return self.calculate_cost(hours, discount=0.0, tax_rate=tax_rate)

    @abstractmethod
    def _raw_amount(self, hours):
        """Amount before tax and discount."""

    def describe(self):
        state = "available" if self._available else "unavailable"
        return (
            f"{self.__class__.__name__} {self.name}: "
            f"{int(self._base_rate)} COP/hour, {state}"
        )


class RoomBooking(Service):
    """Meeting or training room, charged by the hour."""

    def _raw_amount(self, hours):
        return self._base_rate * hours


class EquipmentRental(Service):
    """Devices charged by the hour and by the number of units."""

    def __init__(self, identifier, name, base_rate, units=1, available=True):
        super().__init__(identifier, name, base_rate, available)
        if units is None:
            raise MissingParameterError("units are required")
        if units <= 0:
            raise InconsistentCalculationError("units must be greater than zero")
        self._units = int(units)

    @property
    def units(self):
        return self._units

    def _raw_amount(self, hours):
        return self._base_rate * hours * self._units

    def describe(self):
        text = super().describe()
        return f"{text}, {self._units} unit(s)"


class SpecializedConsulting(Service):
    """Advisory session. Longer sessions add a flat extra fee."""

    MAX_HOURS = 8
    LONG_SESSION_HOURS = 3
    LONG_SESSION_FEE = 40000

    def validate(self, hours, discount=0.0, tax_rate=0.19):
        super().validate(hours, discount, tax_rate)
        if hours > self.MAX_HOURS:
            raise InvalidReservationError(
                f"a consulting session cannot exceed {self.MAX_HOURS} hours"
            )

    def _raw_amount(self, hours):
        extra = self.LONG_SESSION_FEE if hours >= self.LONG_SESSION_HOURS else 0
        return self._base_rate * hours + extra
