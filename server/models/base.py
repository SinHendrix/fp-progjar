from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import settings
import sqlalchemy as sa

Base = None

def init():
    Base = declarative_base()
    engine = sa.create_engine(settings.SQLITE_URI)
    Base.metadata.bind = engine
    session = orm.scoped_session(orm.sessionmaker())(bind=engine)
