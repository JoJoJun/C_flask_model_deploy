from project.models.model import Project,User,SQLAlchemy,Model,Record
from flask_login import current_user
from project.models import db
from datetime import datetime
# 用户名下所有项目信息
def list_all_project():
    # list = Project.query.filter_by(state=0,user=current_user.account).all()
    list = db.session.query(Project).filter_by(state=0,user=current_user.account).all()
    data = []
    for l in list:
        d = {}
        d['name'] = l.name
        d['url'] = l.route
        d['create_time'] = str(l.create_time)
        d['update_time'] = str(l.update_time)
        d['id'] = l.id
        d['description']=l.description
        data.append(d)
    print(data)
    return data

# 根据id得到项目信息
def get_detail_byid(project_id):
    # l = Project.query.filter_by(state=0,id=project_id).first()
    l = db.session.query(Project).filter_by(state=0,id=project_id).first()
    d = {}
    d['name'] = l.name
    d['url'] = l.route
    d['create_time'] = str(l.create_time)
    d['update_time'] = str(l.update_time)
    d['id'] = l.id
    d['description'] = l.description
    # print(d)
    return d


# user name的project是否已存在
def check_project_same_name(name,user_account):
    # return Project.query.filter_by(name=name, user=user_account).first()
    return db.session.query(Project).filter_by(name=name, user=user_account).first()

def goDeletePro(pid):
    # Project.query.filter_by和session不能同时使用

    # 空项目  没有模型
    models =  db.session.query(Model).filter(Model.project == pid).all()
    if len(models)==0:
        print("empty model")
        list2 = db.session.query(Project).filter(Project.id == pid).all()
        [db.session.delete(p) for p in list2]
        db.session.commit()
    else:
        model_id_list = [model.id for model in models]
        [db.session.delete(p) for id in model_id_list for p in db.session.query(Record).filter(Record.model ==id)]
        [db.session.delete(p) for p in models]
        list2 = db.session.query(Project).filter(Project.id == pid).all()
        [db.session.delete(p) for p in list2]
        db.session.commit()
    # 模型下没有实例

    # list = db.session.query(Project, Model, Record).filter(Project.id == Model.project, Model.id == Record.model).filter(
    #     Project.id == pid).all()
    # print(list)
    # [db.session.delete(p) for p in list]
    # db.session.commit()

    if db.session.query(Project).filter_by(id=pid).first():
        return False
    else:
        return True
def edit_Pro(id,name,des):
    flag  = False
    pro = db.session.query(Project).filter_by(id=id).first()
    print(id + ' ' + pro.name + ' ' + pro.route + ' ' + pro.description)
    pro.name = name
    pro.description = des
    print(id + ' ' + pro.name + ' ' + pro.route + ' ' + pro.description)
    db.session.commit()
    if db.session.query(Project).filter_by(name=name).first():
        flag = True
    return flag

def list_all_model(project_id):
    # list = Model.query.filter_by(state=0,project=project_id).all()
    list = db.session.query(Model).filter_by(state=0,project=project_id).all()
    data = []
    for l in list:
        d = {}
        d['name'] = l.name
        d['type'] = l.type
        d['algorithm'] = l.algorithm
        d['RTengine'] = l.RTengine
        d['description'] = l.description
        d['version'] = l.version
        d['assessment'] = l.assessment
        d['create_time'] = str(l.create_time)
        d['update_time'] = str(l.update_time)
        d['id'] = l.id
        data.append(d)
    print(data)
    return data

#检查是否跟其他项目重名
def check_name(new_name, user_account,id):
    # project = Project.query.filter_by(id=id).first()
    project = db.session.query(Project).filter_by(id=id).first()
    if new_name == project.name:
        return False
    elif check_project_same_name(new_name,user_account):
        return True
    return False