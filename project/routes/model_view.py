from project.models.model import User
from flask import Flask, redirect, url_for,render_template,request,Blueprint
## 登录的路由和逻辑都在这页了
import flask_login
import datetime
from project.services.model_service import list_all_model
from project.models import db
model_bp = Blueprint('model', __name__, url_prefix='/model')
# 登录后的全部项目列表页
@model_bp.route('/view/<project_id>', methods=['GET', 'POST'])
def model_view(project_id):
   list = list_all_model(project_id)
   return render_template('model.html', user=flask_login.current_user, data=list)