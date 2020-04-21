from project.models.model import Project,User,SQLAlchemy
from flask_login import current_user
from project.models import db
from datetime import datetime

def list_all_project():
    # user = User.query.filter_by(account = current_user).first()
    list = Project.query.filter_by(state=0,user=current_user.account).all()
    data = []
    for l in list:
        d = {}
        d['name'] = l.name
        d['route'] = l.route
        d['create_time'] = str(l.create_time)
        d['update_time'] = str(l.update_time)
        d['id'] = l.id
        data.append(d)
    print(data)
    return data


# user name的project是否已存在
def check_project_same_name(name,user_account):
    return Project.query.filter_by(name=name, user=user_account).first()

def goDeletePro(pid):
    # Project.query.filter_by和session不能同时使用
    pro = db.session.query(Project).filter_by(id=pid).first()
    db.session.delete(pro)
    db.session.commit()

    if Project.query.filter_by(id=pid).first():
        return False
    else:
        return True