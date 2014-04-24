from models import Base, Enum
from sqlalchemy import Column, DateTime, Integer, String, TypeDecorator, func

class Password(TypeDecorator):
    impl = String

    def bind_expression(self, value):
        return func.crypt(value, func.gen_salt('bf'))

    class comparator_factory(String.comparator_factory):
        def __eq__(self, other):
            crypted_password = type_coerce(self.expr, String)
            return crypted_password == func.crypt(other, crypted_password)

class Role(Enum):
    admin           = ()
    manager         = ()
    employee        = ()
    client_manager  = ()
    client_employee = ()

class Status(Enum):
    pending     = ()
    active      = ()
    suspended   = ()
    deleted     = ()

class User(Base):
    id         = Column(Integer, primary_key=True)
    email      = Column(String)
    fullname   = Column(String)
    password   = Column(Password, nullable=False)
    role       = Column(Role.enum_type(), default=Role.client_manager)
    status     = Column(Status.enum_type(), default=Status.pending)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
