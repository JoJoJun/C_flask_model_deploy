from project.models.model import Project,User
from flask_login import current_user
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
        data.append(d)
    print(data)
    return data