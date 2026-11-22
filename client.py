"""Client records. Personal fields stay behind properties."""

import re

from entity import Entity
from exceptions import InvalidClientDataError, MissingParameterError

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Client(Entity):
    def __init__(self, identifier, name, document, email, phone):
        super().__init__(identifier, name)
        self._document = self._check_document(document)
        self._email = self._check_email(email)
        self._phone = self._check_phone(phone)

    @property
    def document(self):
        return self._document

    @property
    def email(self):
        return self._email

    @property
    def phone(self):
        return self._phone

    def describe(self):
        return f"{self.name} (doc {self.document}, {self.email})"

    @staticmethod
    def _check_document(document):
        if document is None or str(document).strip() == "":
            raise MissingParameterError("document is required")
        value = str(document).strip()
        if not value.isdigit() or not 6 <= len(value) <= 12:
            raise InvalidClientDataError(
                "document must contain between 6 and 12 digits"
            )
        return value

    @staticmethod
    def _check_email(email):
        if email is None or str(email).strip() == "":
            raise MissingParameterError("email is required")
        value = str(email).strip().lower()
        if _EMAIL.match(value) is None:
            raise InvalidClientDataError(f"email '{email}' is not valid")
        return value

    @staticmethod
    def _check_phone(phone):
        if phone is None or str(phone).strip() == "":
            raise MissingParameterError("phone is required")
        value = str(phone).strip().replace(" ", "")
        if not value.isdigit() or not 7 <= len(value) <= 10:
            raise InvalidClientDataError(
                "phone must contain between 7 and 10 digits"
            )
        return value
