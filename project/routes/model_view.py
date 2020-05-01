from flask import render_template,request,Blueprint,jsonify,redirect
import flask_login
import datetime
from project.models.model import Model
from project.services.model_service import getVersion,checkAdd,getFile

from project.models import db
model_bp = Blueprint('model', __name__, url_prefix='/model')
# 登录后的全部项目列表页

@model_bp.route('/checkVersion/',methods=['GET', 'POST'])
def checkVersion():#检查版本
    if request.method == 'GET':
        return render_template('create_model.html', user=flask_login.current_user)
    res = {}
    try:
        pid = request.form['pid']
        name = request.form['name']

        if (len(pid) == 0 or len(name) == 0):
            res['code'] = '100x'
            res['msg'] = '参数数据缺失'
        else:
            version = getVersion(pid, name) + 1
            res['code'] = 1000
            res['msg'] = '查询成功'
            res['data'] = version
    except:
        res['code'] = '100x'
        res['msg'] = '服务器错误，请检查参数'
    return jsonify(res)

@model_bp.route('/addModel/', methods=['GET', 'POST'])#导入模型
def addModel():
    if request.method == 'GET':
        return render_template('create_model.html', user=flask_login.current_user)
    res = {}
    try:
        name = request.form['name']
        type = request.form['type']
        algorithm = request.form['algorithm']
        RTengine = request.form['RTengine']
        des = request.form['description']
        version = request.form['version']  # 需要再发一遍回来吧，确认用？
        assessment = request.form['assessment']
        fileUrl = '/url'#这个file是前端给url还是后端写个接口？
        pid = request.form['project_id']
        if (len(type) == 0 or len(name) == 0 or len(algorithm)==0 or len(RTengine)==0 or len(version)==0 or len(assessment)==0 or len(pid)==0):
            res['code'] = '100x'
            res['msg'] = '参数数据缺失'
        else:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fid = getFile(fileUrl,name)
            new_model = Model(project=pid, name=name, type=type, description=des, algorithm=algorithm, RTengine=RTengine,
                          version=version, assessment=assessment,file=fid, create_time=dt, update_time=dt)
            db.session.add(new_model)
            db.session.commit()
            flag = checkAdd(pid, name, version)

            if flag:
                res['code'] = 1000
                res['msg'] = '创建成功'
            else:
                res['code'] = 1004
                res['msg'] = '创建失败'
    except:
        res['code'] = '100x'
        res['msg'] = '服务器错误，请检查参数'
    return jsonify(res)