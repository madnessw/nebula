from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.types import TypeDecorator, Integer
import enum
import re

@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(self):
        name = re.sub('(?<!^)(?=[A-Z])', '_', self.__name__).lower()
        if re.search('[sxz]$', name):
            return re.sub('$', 'es', name)
        elif re.search('[^aeioudgkprt]h$', name):
            return re.sub('$', 'es', name)
        elif re.search('[^aeiou]y$', name):
            return re.sub('y$', 'ies', name)
        else:
            return name + 's'

class _define_enum_type(TypeDecorator):
    impl = Integer

    def __init__(self, enum):
        self.enum = enum

    def process_bind_param(self, member, dialect):
        assert member in self.enum
        return member.value

    def process_result_value(self, value, dialect):
        return self.enum(value);

class Enum(enum.Enum):
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value

        return obj

    @classmethod
    def enum_type(self):
        return _define_enum_type(self)
