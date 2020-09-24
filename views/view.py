import json

from flask import Flask, request, render_template, redirect, url_for, flash, jsonify

# from form.login_form import LoginForm
from sqlalchemy import or_

from model import User, Project, InterFace
from setting import app, db


@app.route('/', methods=['POST', 'GET'])
def index():
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     print(username)
    #     password = request.form.get('password')
    #     email = request.form.get('email')
    #     user = User(username=username, password=password, email=email)
    #     db.session.add(user)
    #     db.session.commit()
    #     return redirect('home.html')
    return render_template('add/add_test_case.html')


@app.route('/del_user/<id>')
def delete_user(id):
    try:
        # get_id = request.args.get('id')
        del_user = User.query.get(id)
        db.session.delete(del_user)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        raise e
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'post':
        username = request.form.get('username')
        password = request.form.get('password')
        if username or password is not None:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('home.html')
    else:
        return render_template('login.html', msg='请输入正确信息')


@app.route('/getUserInfo')
def getUsersInfo():
    users_list = User.query.all()
    return render_template('add/../templates/user/userInfo.html', users=users_list)


@app.route('/save_user', methods=['POST', 'GET'])
def save_user():
    data = request.get_data()
    res = (data.decode())
    return redirect('/users_info')


@app.route('/getInterfaceDetail', methods=['POST', 'GET'])
def getInterfaceDetail():
    if request.method == 'GET':
        interfaces = InterFace.query.all()
        projects = Project.query.all()
        return render_template('add/InterfaceDetail.html', interfaces=interfaces, projects=projects)
    else:
        pass
    return render_template('add/InterfaceDetail.html')


@app.route('/getProjectDetail', methods=['POST', 'GET'])
def getProjectDetail():
    if request.method == 'GET':
        projects = Project.query.all()
        return render_template('add/projectDetail.html', projects=projects)
    else:
        projectname = request.form.get('projectname')
        select_projectName = Project.query.filter_by(project_name=projectname).all()
        if not select_projectName:
            project = Project(project_name=projectname)
            db.session.add(project)
            db.session.commit()
            return render_template('add/projectDetail.html')
        else:
            return render_template('add/projectDetail.html')


@app.route('/createProject', methods=['POST'])
def createProject():
    if request.method == 'POST':
        project_name = request.form.get('projectname')
        return project_name
    return 'hello'


@app.route('/search')
def search():
    keyword = request.args.get('search')
    users_list = User.query.filter(User.username.contains(keyword)).all()
    return render_template('add/../templates/user/userInfo.html', users=users_list)


@app.route('/searchProject', methods=['POST', 'GET'])
def searchProject():
    keyword = request.args.get('search')
    projects = Project.query.filter(Project.projectname.contains(keyword)).all()
    return render_template('add/projectDetail.html', projects=projects)


@app.route('/editProject', methods=['GET', 'POST'])
def editProject():
    if request.method == 'POST':
        id = request.form.get('id')
        project = Project.query.get(id)
        projectname = request.form.get('projectname')
        project.projectname = projectname
        db.session.commit()
        return redirect(url_for('getProjectDetail'))
    else:
        id = request.args.get('id')
        project = Project.query.get(id)
        return render_template('update/update_project.html', project=project)


@app.route('/delete/<int:id>')
def deleteProject(id):
    project = Project.query.get(id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('getProjectDetail'))
