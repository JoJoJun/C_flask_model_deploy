from project.models.model import User,Record
from flask import Flask, redirect, url_for,render_template,request,Blueprint,jsonify
from project.models import db
import flask_login
import datetime
record_bp = Blueprint('record', __name__, url_prefix='/record')
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