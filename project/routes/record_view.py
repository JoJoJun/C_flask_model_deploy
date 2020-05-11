from project.models.model import User
from flask import Flask, redirect, url_for,render_template,request,Blueprint,jsonify
from project.models.model import User,Record
from flask import Flask, redirect, url_for,render_template,request,Blueprint,jsonify
from project.models import db
import flask_login
import datetime
from project.services.record_service import get_record_detail_by_model,get_record_state,get_record_by_id
record_bp = Blueprint('record', __name__, url_prefix='/record')
from project.services.record_service import countStat,get_Record_State

@record_bp.route('/startModel/',methods=['GET', 'POST'])
def startModel():#模型部署
    res = {}
    try:
        id = request.form['model_id']
        if (len(id) == 0):
            res['code'] = 1005
            res['msg'] = '参数数据缺失'
        else:
            #先查部署的模型有没有超过10
            count = countStat(id)

            if count>=10:
                res['code'] = 2016
                res['msg'] = '运行实例数达到上限'
            elif get_Record_State(id):
                res['code'] = 2015
                res['msg'] = '该模型已经在运行状态'
            else:
                model_setting_file_path = ''
                user_pid_list = ''
                program_pid_list = ''
                code = deploy(id,model_setting_file_path,user_pid_list,program_pid_list)  #部署系统返回的代码
                if code == '4033':
                    res['code'] = 1003
                    res['msg'] = '部署失败'
                else:
                    #获得pid port和url和时间，存到数据库
                    res['code'] = 1000
                    res['msg'] = '部署成功'
    except:
        res['code'] = 2000
        res['msg'] = '服务器错误，请检查参数'
    return jsonify(res)

def deploy(id,model_setting_file_path,user_pid_list,program_pid_list):#模型部署
    return '4033'

#states，pid，url，key


# 暂停运行中实例
@record_bp.route('/pauseModel/<record_id>',methods=['GET','POST'])
def pauseModel(record_id):
    res = {}
    print(record_id)
    # record = get_record_detail_by_model(model_id)
    record = get_record_by_id(record_id)
    # 判断查询是否成功
    if not record:
        code = 2012
        msg = '服务未启动'
        res['code']=code
        res['msg']=msg
        return jsonify(res)

    port = record.port
    state = get_record_state(record_id)
    print(state,type(state))
    # 判断实例状态
    # 2 暂停中
    if state == 2:
        res['code'] = 2014
        res['msg'] = '实例已在暂停状态'
        return jsonify(res)
    # 0 未部署
    elif state == 0:
        code = 2012
        msg = '服务未启动'
        res['code'] = code
        res['msg'] = msg
        return jsonify(res)
    else:
        # TODO 调用pause(record_id,port) 返回ans
        ans = False
        if ans:
            res['code'] = 1000
            res['msg'] = '实例暂停成功'
        else:
            res['code'] = 2000
            res['msg'] = '实例暂停失败'
        return jsonify(res)



# 测试数据库修改
@record_bp.route('/addtest/', methods=['GET', 'POST'])
def addrecord():
    if request.method == 'GET':
      return render_template('create_project.html',user = flask_login.current_user)
    model = request.form['model']
    url = request.form['url']
    output = request.form['output']
    input = request.form['input']
    key = request.form['key']
    port = request.form['port']
    create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(model, url, output,input,key,port,create_time)
    new_record = Record(model = model, url = url, output = output, input = input,key = key, port=port,create_time=create_time)
    db.session.add(new_record)
    db.session.commit()
    dic  = {}
    msg = 'true'
    dic['msg']=msg
    return jsonify(dic)