from flask import render_template,request,Blueprint,jsonify,redirect
import flask_login
import datetime
from project.models.model import Model
from project.services.model_service import getVersion,checkAdd,getFile,delete_model,findRecord,edit_param

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
        des = request.form['description']
        version = request.form['version']  # 需要再发一遍回来吧，确认用？
        fileUrl = '/url'#这个file是前端给url还是后端写个接口？
        pid = request.form['project_id']
        if (len(type) == 0 or len(name) == 0 or len(version)==0 or len(fileUrl)==0 or len(pid)==0):
            res['code'] = '100x'
            res['msg'] = '参数数据缺失'
        else:
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(name)
            fid = getFile(fileUrl,name)
            new_model = Model(project=pid, name=name, type=type, description=des,
                          version=version, file=fid, create_time=dt, update_time=dt)
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


@model_bp.route('/deleteModel/', methods=['GET', 'POST'])#删除模型
def deleteModel():
    if request.method == 'GET':
        return render_template('create_model.html', user=flask_login.current_user)
    res = {}
    try:
        id = request.form['model_id']
        if (len(id) == 0):
            res['code'] = '100x'
            res['msg'] = '参数数据缺失'
        else:
            flag = delete_model(id)
            if flag:
                res['code'] = 1000
                res['msg'] = '删除成功'
            else:
                res['code'] = 1004
                res['msg'] = '删除失败'
    except:
        res['code'] = '100x'
        res['msg'] = '服务器错误，请检查参数'
    return jsonify(res)

@model_bp.route('/editParam/', methods=['GET', 'POST'])#设置参数
def editParam():
    if request.method == 'GET':
        return render_template('create_model.html', user=flask_login.current_user)
    res = {}
    try:
        id = request.form['model_id']
        RTenvironment = request.form['RTenvironment']
        cpu = request.form['cpu']
        memory = request.form['memory']
        if (len(id) == 0 or len(RTenvironment) ==0 or len(cpu)==0 or len(memory)==0):
            res['code'] = '100x'
            res['msg'] = '参数数据缺失'
        else:
            flag = findRecord(id)
            if flag:   #已经有了，修改
                if edit_param(id,RTenvironment,cpu,memory):
                    res['code'] = '1000'
                    res['msg'] = '操作成功'
                else:
                    res['code'] = '1004'
                    res['msg'] = '修改失败'
            else:   #还没有，新增
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_Record = Model(model=id, RTenvironment=RTenvironment, cpu=cpu, memory=memory,
                                   state = 0,create_time=dt, update_time=dt)
                db.session.add(new_Record)
                db.session.commit()
                if findRecord(id):
                    res['code'] = '1000'
                    res['msg'] = '操作成功'
                else:
                    res['code'] = '1004'
                    res['msg'] = '添加失败'
    except:
        res['code'] = '100x'
        res['msg'] = '服务器错误，请检查参数'
    return jsonify(res)