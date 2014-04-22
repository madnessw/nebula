from models import Base
from sqlalchemy import Column, DateTime, Enum, Integer, String, func

class Password(TypeDecorator):
    impl = String

    def bind_expression(self, value):
        return func.crypt(value, func.gen_salt('bf'))

    class comparator_factory(String.comparator_factory):
        def __eq__(self, other):
            local_pw = type_coerce(self.expr, String)
            return local_pw == func.crypt(other, local_pw)

class User(Base):
    id         = Column(Integer, primary_key=True)
    email      = Column(String)
    fullname   = Column(String)
    password   = Column(Password, nullable=False)
    status     = Column(Enum('pending', 'active', 'suspended', 'deleted'), default='pending')
    role       = Column(Enum('manager', 'employee', 'client'), default='client')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.current_timestamp())
