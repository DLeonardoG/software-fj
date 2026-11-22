"""A reservation ties one client to one service for a number of hours."""

from event_log import get_logger
from exceptions import (
    InvalidReservationError,
    MissingParameterError,
    OperationNotAllowedError,
    SoftwareFJError,
)


class Reservation:
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    PROCESSED = "processed"

    def __init__(self, code, client, service, hours):
        if code is None or str(code).strip() == "":
            raise MissingParameterError("reservation code is required")
        if client is None or service is None:
            raise MissingParameterError("client and service are required")
        if hours is None or hours <= 0:
            raise InvalidReservationError("duration must be greater than zero")
        self._code = str(code).strip()
        self._client = client
        self._service = service
        self._hours = hours
        self._status = self.PENDING
        self._total = None

    @property
    def code(self):
        return self._code

    @property
    def client(self):
        return self._client

    @property
    def service(self):
        return self._service

    @property
    def hours(self):
        return self._hours

    @property
    def status(self):
        return self._status

    @property
    def total(self):
        return self._total

    def confirm(self):
        log = get_logger()
        try:
            if self._status != self.PENDING:
                raise OperationNotAllowedError(
                    f"reservation {self._code} cannot be confirmed "
                    f"from status {self._status}"
                )
            total = self._service.calculate_cost(self._hours)
        except OperationNotAllowedError as error:
            log.error("confirm rejected for %s: %s", self._code, error)
            raise
        except SoftwareFJError as error:
            log.error("confirm failed for %s: %s", self._code, error)
            raise InvalidReservationError(
                f"reservation {self._code} was not confirmed"
            ) from error
        else:
            self._status = self.CONFIRMED
            self._total = total
            log.info("reservation %s confirmed, total %s", self._code, total)
            return total
        finally:
            log.info("confirm finished for %s", self._code)

    def cancel(self):
        log = get_logger()
        try:
            if self._status in (self.CANCELLED, self.PROCESSED):
                raise OperationNotAllowedError(
                    f"reservation {self._code} cannot be cancelled "
                    f"from status {self._status}"
                )
        except OperationNotAllowedError as error:
            log.error("cancel rejected for %s: %s", self._code, error)
            raise
        else:
            previous = self._status
            self._status = self.CANCELLED
            log.info("reservation %s cancelled from %s", self._code, previous)
            return self._status
        finally:
            log.info("cancel finished for %s", self._code)

    def process(self):
        log = get_logger()
        try:
            if self._status != self.CONFIRMED:
                raise OperationNotAllowedError(
                    f"only a confirmed reservation can be processed; "
                    f"{self._code} is {self._status}"
                )
            total = self._service.calculate_cost(self._hours)
        except SoftwareFJError as error:
            log.error("process failed for %s: %s", self._code, error)
            raise
        else:
            self._total = total
            self._status = self.PROCESSED
            log.info("reservation %s processed, total %s", self._code, total)
            return total
        finally:
            log.info("process finished for %s", self._code)

    def describe(self):
        total = "n/a" if self._total is None else str(self._total)
        return (
            f"{self._code}: {self._client.name} / {self._service.name}, "
            f"{self._hours} h, {self._status}, total {total}"
        )
