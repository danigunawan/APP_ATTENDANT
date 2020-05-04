from easydict import EasyDict as edict 
def get_config():
    conf=edict()
    conf.database_path="sqlite:///database/attendance.db"
    return conf