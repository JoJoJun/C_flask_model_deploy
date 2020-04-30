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


# 由项目id模型列表
def model_list(pro_id):
    list = Model.query.filter_by(state=0, project=pro_id).all()
    data = []
    for l in list:
        d = {}
        d['name'] = l.name
        d['type'] = l.type
        d['create_time'] = str(l.create_time)
        d['update_time'] = str(l.update_time)
        d['id'] = l.id
        d['algorithm']=l.algorithm
        d['RTengine']=l.RTengine
        d['description']=l.description
        d['version']=l.version
        d['assessment']=l.assessment
        # d['file']=l.file
        # d['project']=l.project
        data.append(d)
    # print(data)
    return data
