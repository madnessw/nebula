from base.middleware import StripPathMiddleware
from base.plugins import SQLAlchemyPlugin
from bottle import default_app, install, run
from sqlalchemy import create_engine
import controllers

_engine = create_engine('postgresql://xxx:zzz@localhost/nebula')

install(SQLAlchemyPlugin(_engine))

app = StripPathMiddleware(default_app())
run(app=app, debug=True)
