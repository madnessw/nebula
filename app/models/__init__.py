from sqlalchemy.ext.declarative import as_declarative, declared_attr
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
