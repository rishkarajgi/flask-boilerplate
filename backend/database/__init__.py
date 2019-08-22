# alias common names
from sqlalchemy import UniqueConstraint, orm
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

from backend.extensions import db
from backend.magic import Bundle

from .audit_log import AuditableMixin
from .base_model import BaseModel
from .column import Column
from .events import attach_events, on, slugify
from .mixins import GUIDMixin, PrimaryKeyMixin, TimestampMixin
from .model import Model
from .relationships import backref, foreign_key, relationship
from .types import (GUID, BigInteger, Boolean, Date, DateTime, Enum, Float,
                    ForeignKey, Integer, Interval, Numeric, SmallInteger,
                    String, Text, Time)

# pylint: disable=invalid-name
session = db.session  # type: orm.session.Session

bundle = Bundle(__name__)

__all__ = [
    'UniqueConstraint',
    'orm',
    'association_proxy',
    'declared_attr',
    'hybrid_method',
    'hybrid_property',
    'db',
    'AuditableMixin',
    'BaseModel',
    'Column',
    'attach_events',
    'on',
    'slugify',
    'GUIDMixin',
    'PrimaryKeyMixin',
    'TimestampMixin',
    'Model',
    'backref',
    'foreign_key',
    'relationship',
    'GUID',
    'BigInteger',
    'Boolean',
    'Date',
    'DateTime',
    'Enum',
    'Float',
    'ForeignKey',
    'Integer',
    'Interval',
    'Numeric',
    'SmallInteger',
    'String',
    'Text',
    'Time',
    'session',
    'bundle'
]
