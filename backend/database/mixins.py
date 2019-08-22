import uuid

from sqlalchemy import func

from .column import Column
from .types import GUID, BigInteger, DateTime


class PrimaryKeyMixin(object):
    """
    Adds an :attr:`id` primary key column to a Model
    """
    id = Column(BigInteger, primary_key=True)


class TimestampMixin(object):
    """
    Adds automatically timestamped :attr:`created_at` and :attr:`updated_at`
    columns to a Model
    """
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())


class GUIDMixin(object):
    """
    Adds a GUID column to a Model
    """
    id = Column(GUID, primary_key=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = uuid.uuid4()
