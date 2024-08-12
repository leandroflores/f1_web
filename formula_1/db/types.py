import datetime

from formula_1.utils import Hash
from sqlalchemy.types import DateTime, Text, TypeDecorator
from typing import Any

class HashedStr(TypeDecorator):
    """Allows storing and retrieving hashes using Hash."""

    impl = Text

    def __init__(self, **kwds):
        super(HashedStr, self).__init__(**kwds)

    def process_bind_param(self, value, dialect):
        return self._convert(value).hash_value

    def process_result_value(self, value, dialect):
        if value is not None:
            return Hash(value)

    def validator(self, password):
        return self._convert(password)

    def compare_values(self, x: Any, y: Any) -> bool:
        if isinstance(x, Hash) and isinstance(y, Hash):
            return x.hash_value == y.hash_value
        elif isinstance(x, str) and isinstance(y, str):
            return x == y
        elif x is None and y is None:
            return True
        return False

    def _convert(self, value):
        if isinstance(value, Hash):
            return value
        elif isinstance(value, str):
            return Hash.new(value)
        elif value is not None:
            raise TypeError(
                "Cannot convert {} to a Hashed".format(type(value))
            )


class TZDateTime(TypeDecorator):
    """Allows storing and retrieving datetimes with timezone information."""

    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("tzinfo is required")
            value = value.astimezone(datetime.UTC).replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=datetime.UTC)
        return value
