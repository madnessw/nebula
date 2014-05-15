from enum import IntEnum
from models import Base
from sqlalchemy import Column, DateTime, Integer, String, TypeDecorator, func

class Password(TypeDecorator):
    impl = String

    def bind_expression(self, value):
        return func.crypt(value, func.gen_salt('bf'))

    class comparator_factory(String.comparator_factory):
        def __eq__(self, other):
            crypted_password = type_coerce(self.expr, String)
            return crypted_password == func.crypt(other, crypted_password)

class Enum(TypeDecorator):
    impl = Integer

    def __init__(self, enum):
        self.enum = enum

    def process_bind_param(self, member, dialect):
        assert member in self.enum
        return member.value

    def process_result_value(self, value, dialect):
        return self.enum(value);

class Role(IntEnum):
    admin           = 0
    manager         = 1
    employee        = 2
    client_manager  = 3
    client_employee = 4

class Status(IntEnum):
    pending   = 0
    active    = 1
    suspended = 2
    deleted   = 3

class User(Base):
    id         = Column(Integer, primary_key=True)
    email      = Column(String, nullable=False)
    fullname   = Column(String)
    password   = Column(Password, nullable=False)
    role       = Column(Enum(Role), default=Role.client_manager)
    status     = Column(Enum(Status), default=Status.pending)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
