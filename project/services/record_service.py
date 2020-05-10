from project.models.model import Project,User,SQLAlchemy,Model,File,Record
from project.models import db
from datetime import datetime
# 由model_id返回record
def get_record_detail_by_model(model_id):
    print(model_id)
    record = Record.query.filter_by(model=model_id).first()

    return record
def countStat(id):
    count = 0
    return count

def get_Record_State(id):#True代表
    flag = False

    return flag

# 判断是否已经暂停
def get_record_state(record_id):
    record = Record.query.filter_by(id = record_id).first()
    state = record.state
    state = int(state)
    return state

# 由record_id返回record
def get_record_by_id(record_id):
    return Record.query.filter_by(id = record_id).first()