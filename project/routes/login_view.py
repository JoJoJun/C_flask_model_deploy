import flask_login
from project.models.model import User
from flask import Flask, redirect, url_for,render_template,request,Blueprint,flash
from project.services.project_service import list_all_project
from project.models import db
from datetime import datetime
## 登录的路由和逻辑都在这页了
login_bp = Blueprint('login', __name__, url_prefix='/account')
login_manager = flask_login.LoginManager()


# users = {'foo@bar.tld': {'password': 'secret'}}
@login_manager.user_loader
def load_user(account):
    return User.query.get(account)


# @login_manager.request_loader
# def request_loader(request):
#     account = request.form.get('account')
#     user = User.query.get(account)
#     if not user:
#         return None
#
#     # DO NOT ever store passwords in plaintext and always compare password
#     # hashes using constant-time comparison!
#     user.is_authenticated = request.form['password'] == user.password
#     return user


@login_bp.route('/login/', methods=['GET', 'POST'])
def login():
    print("in login!!!!!")
    if request.method == 'GET':
        return render_template('login.html',user=flask_login.current_user)
    email = request.form['account']
    user_in_db = User.query.filter_by(account=email).first()
    check_pwd = user_in_db.check_password(request.form['password'])
    if not user_in_db:
        msg = '用户不存在'
    if not check_pwd:
        msg = '密码或用户名有误'
    if user_in_db and  check_pwd:
        flask_login.login_user(user_in_db)
        list = list_all_project()
        flash('You were successfully logged in')
        return render_template('index.html',user = flask_login.current_user,data=list)
        # return redirect(url_for('login.protected'))
    return render_template('home.html',user=None, msg = msg)


@login_bp.route('/protected')
@flask_login.login_required
def protected():
    print(flask_login.current_user)
    return 'Logged in as: ' + flask_login.current_user.account


@login_bp.route('/regist/', methods=['GET', 'POST'])
def register():
    user = {'is_authenticated': False, 'username': ''}
    if request.method == 'GET':
        return render_template('regist.html',user=user)
    account = request.form['account']
    password = request.form['password']
    password2 = request.form['password2']
    name = request.form['name']
    msg = ''
    if password == password2:
        code = 2003
        msg = '确认密码错误，请重新输入'
    user = User.query.filter_by(account=account).first()
    if user:
        msg = '账户已注册'
        code = 2002
    else:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user = User(account=account,password=password,name=name,create_time = dt,update_time = dt)
        db.session.add(new_user)
        db.session.commit()
        msg='成功'
        code = 1000
        return redirect(url_for('login.login'))
    return render_template('regist.html',user=user,msg = msg)



@login_bp.route('/logout/')
def logout():
    flask_login.logout_user()
    return 'Logged out'