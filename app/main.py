from bottle import install, run, HTTPError
from inspect import getfullargspec
from models import Session
from pkgutil import walk_packages
from sqlalchemy.exc import SQLAlchemyError
import controllers

class StripPathMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['PATH_INFO'] = environ['PATH_INFO'].rstrip('/')
        return self.app(environ, start_response)

class DBSession(object):
    name = 'session'
    api = 2

    def apply(self, callback, context):
        if name not in getfullargspec(context['callback']).args:
            return callback

        def wrapper(*args, **kwargs):
            kwargs[name] = session = Session()

            try:
                rv = callback(*args, **kwargs)
                session.commit()
            except (SQLAlchemyError, HTTPError):
                session.rollback()
                raise
            except HTTPResponse:
                session.commit()
                raise
            finally:
                session.close()

            return rv

        return wrapper

install(DBSession())

for (module_loader, name, _) in walk_packages(controllers.__path__):
    module_loader.find_module(name).load_module(name)

run(debug=True)
