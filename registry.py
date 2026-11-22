"""In-memory lists of clients, services and reservations. No database."""

from event_log import get_logger
from exceptions import InvalidReservationError, OperationNotAllowedError, SoftwareFJError
from reservation import Reservation


class Registry:
    def __init__(self):
        self._clients = []
        self._services = []
        self._reservations = []
        self._log = get_logger()

    @property
    def clients(self):
        return list(self._clients)

    @property
    def services(self):
        return list(self._services)

    @property
    def reservations(self):
        return list(self._reservations)

    def register_client(self, client):
        try:
            for current in self._clients:
                if current.document == client.document:
                    raise OperationNotAllowedError(
                        f"document {client.document} is already registered"
                    )
        except OperationNotAllowedError as error:
            self._log.error("client not registered: %s", error)
            raise
        else:
            self._clients.append(client)
            self._log.info("client registered: %s", client.describe())
            return client
        finally:
            self._log.info(
                "register_client finished for document %s", client.document
            )

    def add_service(self, service):
        try:
            for current in self._services:
                if current.identifier == service.identifier:
                    raise OperationNotAllowedError(
                        f"service id {service.identifier} already exists"
                    )
        except OperationNotAllowedError as error:
            self._log.error("service not added: %s", error)
            raise
        else:
            self._services.append(service)
            self._log.info("service added: %s", service.describe())
            return service
        finally:
            self._log.info("add_service finished for %s", service.identifier)

    def create_reservation(self, code, client, service, hours):
        try:
            if client not in self._clients:
                raise InvalidReservationError("the client is not registered")
            if service not in self._services:
                raise InvalidReservationError("the service is not registered")
            reservation = Reservation(code, client, service, hours)
        except SoftwareFJError as error:
            self._log.error("reservation %s was not created: %s", code, error)
            raise
        else:
            self._reservations.append(reservation)
            self._log.info("reservation created: %s", reservation.describe())
            return reservation
        finally:
            self._log.info("create_reservation finished for %s", code)
