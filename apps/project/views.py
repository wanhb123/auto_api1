from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify

from apps.project.models import Project
from ext import db

project = Blueprint('project', __name__, url_prefix='/app/project')


@project.route('/getProjectDetail', methods=['POST', 'GET'])
def getProjectDetail():
    if request.method == 'GET':
        projects = Project.query.filter(Project.is_delete == True).order_by(-Project.create_time).all()
        return render_template('add/projectDetail.html', projects=projects)
    else:
        projectname = request.form.get('projectname')
        if projectname:
            project = Project.query.filter_by(project_name=projectname).all()
            if not project:
                project = Project(project_name=projectname)
                db.session.add(project)
                db.session.commit()
                return render_template('add/projectDetail.html')
            else:
                return render_template('add/projectDetail.html')
        else:
            pass


@project.route('/searchProject', methods=['GET', 'POST'])
def searchProject():
    keyword = request.form.get('search')
    if keyword:
        projects = Project.query.filter(Project.project_name.contains(keyword)).all()
        if len(projects) == 0:
            return render_template('add/projectDetail.html', msg='暂无数据')
        else:
            return render_template('add/projectDetail.html', projects=projects)
    else:
        projects = Project.query.order_by(-Project.create_time).all()
        return render_template('add/projectDetail.html', projects=projects)


@project.route('/app/v1/editProject', methods=['GET', 'POST'])
def editProject():
    if request.method == 'POST':
        try:
            id = request.form.get('id')
            project = Project.query.get(id)
            projectname = request.form.get('projectname')
            project.project_name = projectname
            db.session.commit()
            return redirect(url_for('user.getProjectDetail'))
        except Exception as e:
            return jsonify({'data': e.args[0], 'msg': '项目已存在'})
    else:
        id = request.args.get('id')
        project = Project.query.get(id)
        return render_template('update/update_project.html', project=project)


@project.route('/deleteProject/<int:id>')
def deleteProject(id):
    # id = request.args.get('projectid')
    project = Project.query.get(id)
    project.is_delete = False
    # db.session.delete(project)
    db.session.commit()
    return redirect(url_for('user.getProjectDetail'))