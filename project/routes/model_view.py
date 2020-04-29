from flask import render_template,request,Blueprint,jsonify
import flask_login
import datetime
from project.models.model import Model
from project.services.model_service import getVersion,checkAdd

from project.models import db
model_bp = Blueprint('model', __name__, url_prefix='/model')
# 登录后的全部项目列表页

@model_bp.route('/checkVersion/',methods=['GET', 'POST'])
def checkVersion():#检查版本
    if request.method == 'GET':
        return render_template('create_model.html', user=flask_login.current_user)
    pid = request.form['pid']
    name = request.form['name']

    print(name)
    version = getVersion(pid,name)+1
    res = {}
    res['code'] = 1000
    res['msg'] = '查询成功'
    res['data'] = version
    return jsonify(res)

@model_bp.route('/addModel/', methods=['GET', 'POST'])
def addModel():
    if request.method == 'GET':
        return render_template('create_model.html', user=flask_login.current_user)
    name = request.form['name']
    type = request.form['type']
    algorithm = request.form['algorithm']
    RTengine = request.form['RTengine']
    des = request.form['description']
    version = request.form['version'] #需要再发一遍回来吧
    assessment = request.form['assessment']
    pid = request.form['project_id']
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_model = Model(project = pid,name=name, type=type, description=des, algorithm=algorithm,RTengine= RTengine, version=version,assessment=assessment,create_time=dt, update_time=dt)
    db.session.add(new_model)
    db.session.commit()
    flag = checkAdd(pid,name,version)
    res = {}
    if flag:
        res['code'] = 1000
        res['msg'] = '创建成功'
    else:
        res['code'] = 1004
        res['msg'] = '创建失败'
    return jsonify(res)