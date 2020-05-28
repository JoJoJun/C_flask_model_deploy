from project.models.model import User,Project,Model,Record
from flask import Flask, redirect, url_for,render_template,request,Blueprint,jsonify

from project.services.project_service import list_all_project, check_project_same_name,goDeletePro,edit_Pro,get_detail_byid,check_name
import flask_login
import datetime
from project.models import db
from project.services.model_service import model_list
project_bp = Blueprint('project', __name__, url_prefix='/project')


# 登录后的全部项目列表页
@project_bp.route('/', methods=['GET', 'POST'])
def project_view():
   if not flask_login.current_user.is_authenticated:
       return redirect(url_for('login.login'))
   list = list_all_project()
   return render_template('index.html', user=flask_login.current_user, data=list)


# 新建项目
@project_bp.route('/addPro/', methods=['GET', 'POST'])
def addPro():
   if request.method == 'GET':
       return render_template('create_project.html',user = flask_login.current_user)
   if not flask_login.current_user.is_authenticated:
       return redirect(url_for('login.login'))
   print(request.form)
   name = request.form['name']
   url = request.form['url']
   des = request.form['description']
   user_account = flask_login.current_user.account
   res ={}
   if check_project_same_name(name,user_account):
      code = 2004
      msg='用户名下已存在同名项目'
      res['code']=code
      res['msg']=msg
      return jsonify(res)
      #return render_template('create_project.html',user = flask_login.current_user,res=res)
   else:
      dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      new_project = Project(name=name,url=url,des=des,user=user_account,create_time=dt,update_time=dt)
      db.session.add(new_project)
      db.session.commit()
      code = 1000
      msg='新建项目成功'
      res['code']=code
      res['msg']=msg
      res['id']=db.session.query(Project).filter_by(name=name,user=user_account).first().id
      # return redirect(url_for('project.project_view'))
      return jsonify(res)
   # res['code']=code
   # res['msg']=msg
   # return render_template('index.html',user=flask_login.current_user,res=res)



@project_bp.route('/editPro/', methods=['GET', 'POST'])#编辑项目
def editPro():
   if request.method == 'GET':
      return render_template('index.html',user = flask_login.current_user)
   if not flask_login.current_user.is_authenticated:
      return redirect(url_for('login.login'))
   id = request.form['id']
   name = request.form['name']
   url = request.form['url']
   des = request.form['description']
   res = {}
   if not check_id(id,0,0):
       code = 3000
       msg = '用户身份不匹配，请重试'
       res['code'] = code
       res['msg'] = msg
       return jsonify(res)
   user_account = flask_login.current_user.account
#   user_account = '123@123.com'
   if check_name(name, user_account,id):
       code = 2004
       msg = '用户名下已存在同名项目'
       res['code'] = code
       res['msg'] = msg
       return jsonify(res)
       #return render_template('index.html', user=flask_login.current_user, res=res)
   else:
#       Project.query.filter_by(id=id).update({'name': name,'route':url,'description':des})
       print('ccccccccc')
       flag = edit_Pro(id,name,url,des)
       if flag:
            res['code'] = 1000
            res['msg'] = '操作成功'
       else:
            res['code'] = 1004
            res['msg'] = '操作失败'
       return jsonify(res)


@project_bp.route('/deletePro/',methods = ['POST', 'GET'])#删除项目
def deletePro():
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for('login.login'))
    pid = request.form.get("id")
    print('test'+ pid)
    res = {}
    if not check_id(pid, 0, 0):
        code = 3000
        msg = '用户身份不匹配，请重试'
        res['code'] = code
        res['msg'] = msg
        return jsonify(res)
    if db.session.query(Project, Model,Record).filter(
            Project.id==Model.project,Model.id==Record.model).filter(
            Project.id == pid,  Record.state == '1').first():
        res['code'] = 2013
        res['msg'] = '实例正在运行，无法删除'
        return jsonify(res)
    flag = goDeletePro(pid)

    if flag:  # 删除成功
        res['code'] = 1000
        res['msg'] = '删除成功'
        return jsonify(res)
    else:
        res['code'] = 1004
        res['msg'] = '删除失败'
        return render_template('index.html', user=flask_login.current_user, res=res)


# 查看项目
@project_bp.route('/view/<project_id>',methods = ['POST', 'GET'])
def viewPro(project_id):
    print(project_id)
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for('login.login'))
    l = db.session.query(Project).filter_by(state=0, id=project_id).first()
    if not l:
        return redirect(url_for('login.login'))
    # if l.user != '123@123.com':
    if  l.user != flask_login.current_user.account:
        return redirect(url_for('login.login'))
    modellist = model_list(project_id)
    info= get_detail_byid(project_id)
    info['model_list']=modellist
    return render_template('project.html',user=flask_login.current_user,project_info=info)


def check_id(project_id,model_id,record_id):
    flag = False
    account = flask_login.current_user.account
    if project_id != 0:#验证pid
        if db.session.query(Project).filter_by(state=0, id=project_id, user=account).first():  #该pid属于该用户
            flag = True
    if model_id != 0:#验证mid
        if db.session.query(User,Project, Model).filter(
                User.account == Project.user,Project.id==Model.project).filter(
                User.account == account,Model.id == model_id).first():
            flag = True    #该mid属于该用户
    if record_id != 0:#验证rid
        if db.session.query(User,Project, Model,Record).filter(
                User.account == Project.user,Project.id==Model.project,Model.id == Record.model).filter(
                User.account == account,Record.id == record_id).first():
            flag = True  #该rid属于该用户
    return flag