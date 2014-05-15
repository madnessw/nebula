from bottle import HTTPError, HTTPResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import inspect

#TODO engine routing
class SQLAlchemyPlugin(object):
    name = 'sqlalchemy'
    api = 2

    def __init__(self, engine, keyword='db'):
        self.engine = engine
        self.keyword = keyword

    def setup(self, app):
        for other in app.plugins:
            if not isinstance(other, SQLAlchemyPlugin):
                continue

            if other.keyword == self.keyword:
                raise PluginError("Found another SQLAlchemy plugin with "\
                    "conflicting settings (non-unique keyword).")

    def apply(self, callback, context):
        conf = context.config.get('sqlalchemy') or {}
        keyword = conf.get('keyword', self.keyword)

        if keyword not in inspect.getfullargspec(context.callback).args:
            return callback

        def wrapper(*args, **kwargs):
            kwargs[keyword] = session = sessionmaker(bind=self.engine)

            try:
                rv = callback(*args, **kwargs)
                session.commit()
            except SQLAlchemyError as err:
                session.rollback()
                raise HTTPError(500, "Database Error", err)
            except HTTPError:
                raise
            except HTTPResponse:
                session.commit()
                raise
            finally:
                session.close()

            return rv

        return wrapper
