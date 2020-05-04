from sqlalchemy import create_engine, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .config import get_config



engine = create_engine(get_config().database_path, echo=True, connect_args={'check_same_thread': False},
    poolclass=StaticPool)
Base = declarative_base()
Session = sessionmaker(bind=engine)



