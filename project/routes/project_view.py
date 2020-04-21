from project.models.model import User,Project
from flask import Flask, redirect, url_for,render_template,request,Blueprint

from project.services.project_service import list_all_project, check_project_same_name,goDeletePro
import flask_login
import datetime
from project.models import db
project_bp = Blueprint('project', __name__, url_prefix='/project')
@project_bp.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name


@project_bp.route('/view/')
def project_list():
   list = list_all_project()
   return render_template('index.html',user = flask_login.current_user,data=list)


@project_bp.route('/addPro/', methods=['GET', 'POST'])
def addPro():
   if request.method == 'GET':
      return render_template('create_project.html',user = flask_login.current_user)
   print(request.form)
   name = request.form['name']
   url = request.form['url']
   des = request.form['description']
   print(name,url,des)
   user_account = flask_login.current_user.account
   print(name, url, des)
   # pro = Project.query.filter_by(name=name,user=user_account).first()
   res ={}
   if check_project_same_name(name,user_account):
      code = 2004
      msg='用户名下已存在同名项目'
      res['code']=code
      res['msg']=msg
      return render_template('create_project.html',user = flask_login.current_user,res=res)
   else:
      dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      new_project = Project(name=name,url=url,des=des,user=user_account,create_time=dt,update_time=dt)
      db.session.add(new_project)
      db.session.commit()
      code = 1000
      msg='新建项目成功'
      return redirect(url_for('project.view'))
   # res['code']=code
   # res['msg']=msg
   # return render_template('index.html',user=flask_login.current_user,res=res)



@project_bp.route('/editPro/', methods=['GET', 'POST'])#编辑项目
def editPro():
   if request.method == 'GET':
      return render_template('create_project.html',user = flask_login.current_user)
   id = request.form['project_id']
   name = request.form['Name']
   url = request.form['url']
   des = request.form['description']
   res = {}
   user_account = flask_login.current_user.account
   if check_project_same_name(name, user_account):
       code = 2004
       msg = '用户名下已存在同名项目'
       res['code'] = code
       res['msg'] = msg
       return render_template('index.html', user=flask_login.current_user, res=res)
   else:
       pro = Project.query.filter_by(id=id).first()
       pro.name = name
       pro.url = url
       pro.description = des
       db.session.commit()
       res['code'] = 1000
       res['msg'] = '操作成功'
       return render_template('index.html', user=flask_login.current_user, res=res)

@project_bp.route('/deletePro/',methods = ['POST', 'GET'])#删除项目
def deletePro():
    pid = request.form.get("id")
    print('test'+ pid)
    flag = goDeletePro(pid)
    res = {}


    if flag:  # 删除成功
        res['code'] = 1000
        res['msg'] = '删除成功'
        return render_template('index.html', user=flask_login.current_user, res=res)
    else:
        res['code'] = 1004
        res['msg'] = '删除失败'
        return render_template('index.html', user=flask_login.current_user, res=res)




