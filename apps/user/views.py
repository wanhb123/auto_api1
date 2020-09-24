import json
import requests
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import and_
from sqlalchemy.orm import session
from apps.interface.models import Interface
from apps.project.models import Project
from apps.user.models import User
from ext import db

user = Blueprint('user', __name__, url_prefix='/app/user')


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
    pagination = User.query.order_by(User.createtime.desc()).paginate(page=page, per_page=5)
    return render_template('user/userInfo.html', pagination=pagination)


@user.route('/addUser', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        idCard = request.form.get('idcard')
        if username and password:
            user = User(username=username, password=password, phone=phone)
            db.session.add(user)
            db.session.commit()
        else:
            data = {'msg': '信息不能为空'}
            return jsonify(data)
    return redirect('/getUserInfo')


@user.route('/searchUserInfo', methods=['GET', 'POST'])
def searchUserInfo():
    # keyword = request.args.get('search')
    # users_list = User.query.filter(User.username.contains(keyword)).all()
    # return render_template('add/add_person.html', users=users_list)
    keyword = request.form.get('search')
    page = request.args.get('page')
    if keyword:
        pagination = User.query.filter(User.username.contains(keyword)).paginate(page=page, per_page=5)
        print(type(pagination))
        if pagination == 0:
            return render_template('user/userInfo.html', msg='暂无数据')
        else:
            return render_template('user/userInfo.html', pagination=pagination)
    else:
        pagination = User.query.paginate(page=page, per_page=6)
        return render_template('user/userInfo.html', pagination=pagination)


@user.route('/editUser', methods=['GET', 'POST'])
def editUser():
    if request.method == 'POST':
        try:
            id = request.form.get('id')
            user = User.query.get(id)
            username = request.form.get('username')
            User.username = username
            db.session.commit()
            return redirect(url_for('user.userInfo'))
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
