import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from sqlalchemy import and_
from sqlalchemy.orm import session
from apps.interface.models import Interface
from apps.project.models import Project
from apps.user.models import User
from ext import db

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/index')
def index():
    return render_template('add/base.html')


@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users = User.query.filter(User.username == username).all()
        if users:
            for user in users:
                if user.password == password:
                    return redirect(url_for('user.index'))
                else:
                    return render_template('login.html', msg='用户名或密码有误!')
        else:
            return render_template('login.html', msg='用户名或密码为空!')
    else:
        return render_template('login.html')


@user.route('/getUserInfo')
def getUsersInfo():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.createtime.desc()).paginate(page=page, per_page=2)
    users = pagination.items
    return render_template('user/userInfo.html', pagination=pagination, users=users)


@user.route('/addUser', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        if username and password:
            try:
                phone = User.query.filter(User.phone == phone).first()
                if not phone:
                    user = User(username=username, password=password, phone=phone)
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('user.getUsersInfo'))
                else:
                    render_template('add/addUser.html', msg='手机号已存在')
            except Exception as e:
                print('发生{}异常'.format(e))
        else:
            return render_template('add/addUser.html', msg='信息不能为空')
    else:
        return render_template('add/addUser.html')


@user.route('/searchUserInfo', methods=['GET', 'POST'])
def searchUserInfo():
    keyword = request.form.get('search')
    page = request.args.get('page')
    if keyword:
        pagination = User.query.filter(User.username.contains(keyword)).order_by(User.createtime.desc()).paginate(page, per_page=6)
        if len(pagination.items) == 0:
            return render_template('user/userInfo.html', msg='暂无数据')
        else:
            users = pagination.items
            return render_template('user/userInfo.html', pagination=pagination, users=users)
    else:
        return redirect(url_for('user.getUsersInfo'))


@user.route('/editUser', methods=['GET', 'POST'])
def editUser():
    if request.method == 'POST':
        try:
            id = request.form.get('id')
            user = User.query.get(id)
            username = request.form.get('username')
            user.username = username
            db.session.commit()
            return redirect(url_for('user.getUsersInfo'))
        except Exception as e:
            return jsonify({'data': e.args[0], 'msg': '用户已存在'})
    else:
        id = request.args.get('id')
        user = User.query.get(id)
        return render_template('update/update_user.html', user=user)


@user.route('/forgetPassword', methods=['GET', 'POST'])
def forget():
    if request.method == 'POST':
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        if password or repassword:
            if password == repassword:
                return redirect(url_for('user.login'))
            else:
                return render_template('forgetPassword.html', msg='密码输入不一致')
        else:
            return render_template('forgetPassword.html', msg='密码不能为空！')
    else:
        return render_template('forgetPassword.html')
