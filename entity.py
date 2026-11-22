"""Shared identity for people and services stored by the company."""

from abc import ABC, abstractmethod

from exceptions import MissingParameterError


class Entity(ABC):
    def __init__(self, identifier, name):
        if identifier is None or str(identifier).strip() == "":
            raise MissingParameterError("identifier is required")
        if name is None or str(name).strip() == "":
            raise MissingParameterError("name is required")
        self._identifier = str(identifier).strip()
        self._name = str(name).strip()

    @property
    def identifier(self):
        return self._identifier

    @property
    def name(self):
        return self._name

    @abstractmethod
    def describe(self):
        """Short text used in the simulation output."""
