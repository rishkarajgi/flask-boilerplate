from uuid import UUID


class Validator:
    @classmethod
    def is_invalid(cls, value, validation_type, **kwargs):
        method = getattr(cls, validation_type, None)
        if method:
            return method(value, **kwargs)
        raise Exception('Validation method not found')

    @staticmethod
    def data_type(value, expected_type):
        if expected_type == 'uuid':
            try:
                UUID(value)
            except Exception:
                return "Invalid value '{}' for UUID".format(value)
        return False
