from .base import Base, Session, engine
from .attendance import Attendance

class Query():
    def __init__(self):
        self.session=Session()


    def search_attendance(self,id,date):
        return self.session.query(Attendance).filter(Attendance.id==id,Attendance.date==date)

    def check_attendance(self,id,date):
        x=self.search_attendance(id,date).all()
        if(len(x)>0): return True
        else :return False

    def add(self,object):
        try:
            self.session.add(object)
            self.session.commit()
            print("add done!")
        except Exception as e :
            print(e)
            return -1
    def add_attendance(self,id,date,currtime):
        x=self.search_attendance(id,date)
        if(len(x.all())==0):
            print("Creating")
            att=Attendance(id)
            self.add(att)
        else:
            print("Updating!")
            x.update({Attendance.lasttime:currtime}, synchronize_session = False)
            self.session.commit()

    
    def __close__(self):
        print("close session")
        self.session.close()
        
