from project.models.model import User
from flask import Flask, redirect, url_for,render_template,request,Blueprint
from project.services.project_service import list_all_project
import flask_login
project_bp = Blueprint('project', __name__, url_prefix='/project')
@project_bp.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name


@project_bp.route('/view/')
def project_list():
   list = list_all_project()
   return render_template('index.html',user = flask_login.current_user,data=list)


@project_bp.route('/addPro/')
def addPro():
   name = request.form['Name']
   url = request.form['url']
   des = request.form['description']
   print(name,url,des)