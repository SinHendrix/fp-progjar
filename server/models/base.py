from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import settings
import sqlalchemy as sa

Base = declarative_base()
engine = sa.create_engine(settings.SQLITE_URI, connect_args={'check_same_thread': False})
Base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)
