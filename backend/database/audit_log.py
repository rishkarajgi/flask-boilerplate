from uuid import UUID

import json
from flask import current_app
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.attributes import get_history

from backend.database.events import event, inspect
from backend.extensions.jwt import get_jwt_identity

from .base_model import BaseModel
from .column import Column
from .mixins import GUIDMixin, TimestampMixin
from .types import Integer, String, Text


def _current_user_id_or_none():
    try:
        return get_jwt_identity()
    except:
        return None


class AuditLog(GUIDMixin, TimestampMixin, BaseModel):
    """Model an audit log of user actions"""
    user_id = Column(
        String(100), doc="The ID of the user who made the change", nullable=True)
    target_type = Column(String(100), nullable=False,
                         doc="The table name of the altered object")
    target_id = Column(String(100), doc="The ID of the altered object")
    action = Column(Integer, doc="Create (1), update (2), or delete (3)")
    state_before = Column(Text, doc="Stores a JSON string representation of a dict containing the altered column "
                          "names and original values", nullable=True)
    state_after = Column(Text, doc="Stores a JSON string representation of a dict containing the altered column "
                         "names and new values", nullable=True)

    def __init__(self, target_type, target_id, action, state_before, state_after, created_at=None):
        super().__init__()
        self.user_id = _current_user_id_or_none()
        self.target_type = target_type
        self.target_id = str(target_id)
        self.action = action
        self.state_before = state_before
        self.state_after = state_after
        if self.created_at is not None:
            self.created_at = created_at

    def __repr__(self):
        return '<AuditLog %r: %r -> %r>' % (self.user_id, self.target_type, self.action)

    def save_audit(self, connection):
        connection.execute(
            self.__table__.insert(),
            id=self.id,
            user_id=self.user_id,
            target_type=self.target_type,
            target_id=self.target_id,
            action=self.action,
            state_before=self.state_before,
            state_after=self.state_after
        )


ACTION_CREATE = 1
ACTION_UPDATE = 2
ACTION_DELETE = 3


class AuditableMixin(object):
    """Allow a model to be automatically audited"""

    @staticmethod
    def create_audit(connection, object_type, object_id, action, **kwargs):
        audit = AuditLog(
            object_type,
            object_id,
            action,
            kwargs.get('state_before'),
            kwargs.get('state_after')
        )
        audit.save_audit(connection)

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'after_insert', cls.audit_insert)
        event.listen(cls, 'after_delete', cls.audit_delete)
        event.listen(cls, 'after_update', cls.audit_update)

    @staticmethod
    def audit_insert(mapper, connection, target):
        """Listen for the `after_insert` event and create an AuditLog entry"""
        target.create_audit(connection, target.__tablename__,
                            target.id, ACTION_CREATE)

    @staticmethod
    def audit_delete(mapper, connection, target):
        """Listen for the `after_delete` event and create an AuditLog entry"""
        target.create_audit(connection, target.__tablename__,
                            target.id, ACTION_DELETE)

    @staticmethod
    def audit_update(mapper, connection, target):
        """Listen for the `after_update` event and create an AuditLog entry with before and after state changes"""
        state_before = {}
        state_after = {}
        inspr = inspect(target)
        attrs = class_mapper(target.__class__).column_attrs
        for attr in attrs:
            hist = getattr(inspr.attrs, attr.key).history
            if hist.has_changes():
                value_before = get_history(target, attr.key)[2].pop()
                value_after = getattr(target, attr.key)
                if (isinstance(value_before, UUID) or isinstance(value_after, UUID)) and str(value_before) == str(value_after):
                    continue
                state_before[attr.key] = value_before
                state_after[attr.key] = value_after

        if state_after == state_before:
            return

        target.create_audit(connection, target.__tablename__, target.id, ACTION_UPDATE,
                            state_before=json.dumps(
                                state_before, cls=current_app.json_encoder),
                            state_after=json.dumps(state_after, cls=current_app.json_encoder))
