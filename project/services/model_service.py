from project.models.model import Project,User,SQLAlchemy,Model
from project.models import db
from datetime import datetime

def getVersion(pid,name):#项目id和模型名称
    print(name)
    print(pid)
    count = Model.query.filter_by(state=0,name=name,project = pid).count()
    print(count)
    return count

def checkAdd(pid,name,version):
    flag = False
    if Model.query.filter_by(name=name,project = pid,version=version).all():
        flag = True
    return flag