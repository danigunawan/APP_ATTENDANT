from sqlalchemy import Column, Date, Integer, String, DateTime,PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from .base import Base,engine
import datetime 
from datetime import datetime

class Attendance(Base):
    """"""
    __tablename__ = "attendance"
    __table_args__ = (
        PrimaryKeyConstraint('id', 'date'),
    )
    id = Column("id",String(20), primary_key=True)
    date=Column("date",String(30))
    firsttime=Column("firsttime",String(30))
    lasttime=Column("lasttime",String(30))


    def __init__(self,id):
        now = datetime.now()
        currtime=now.strftime("%H:%M:%S")
        self.id=id
        self.date=now.strftime("%d-%m-%Y")
        self.firsttime=currtime
        self.lasttime=currtime
Base.metadata.create_all(engine)
        