from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from apps.project.models import Project
from ext import db

project_Bp = Blueprint('project', __name__, url_prefix='/project')
project_api = Api(project_Bp)


class GetProjectsApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            page = args.get('page')
            size = args.get('size')
            keyword = args.get('search')
            GMT_FORMAT = "%Y-%m-%d %H:%M:%S"
            if not keyword:
                projects = Project.query.order_by(Project.create_time.desc()).limit(size).offset((page - 1) * size)
                lis = []
                for project in projects:
                    dic = {}
                    dic['id'] = project.id
                    dic['interfaceNum'] = len(project.interface)
                    dic['projectname'] = project.project_name
                    time = datetime.strftime(project.create_time, GMT_FORMAT)
                    dic['createtime'] = time
                    lis.append(dic)
                total = Project.query.count()
            else:
                pagination = Project.query.filter(Project.project_name.contains(keyword)).paginate(page, size)
                projects = pagination.items
                lis = []
                for project in projects:
                    dic = {}
                    dic['interfaceNum'] = len(project.interface)
                    dic['projectname'] = project.project_name
                    time = datetime.strftime(project.create_time, GMT_FORMAT)
                    dic['createtime'] = time
                    dic['id'] = project.id
                    lis.append(dic)
                total = Project.query.filter(Project.project_name.contains(keyword)).count()
            return jsonify({
                'code': 200,
                'msg': '操作成功!',
                'data': lis,
                'total': total
            })
        except Exception as e:
            return ({
                'code': 400,
                'msg': '操作失败!',
                'data': [],
                'total': 0
            })


class GetProjectApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            id = args.get('id')
            project = Project.query.get(id)
            projectname = project.project_name
            return jsonify({
                'code': 200,
                'msg': '操作成功!',
                'projectname': projectname
            })
        except Exception as e:
            return jsonify({
                'code': 400,
                'msg': '操作失败!',
            })


class UpdateProjectApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            id = args.get('id')
            name = args.get('name')
            project = Project.query.get(id)
            project.project_name = name
            db.session.commit()
            return jsonify({
                'code': 200,
                'msg': '操作成功!'
            })
        except Exception as e:
            return jsonify({
                'code': 400,
                'msg': '操作失败!'
            })

class DeleteProjectApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            id = args.get('id')
            project = Project.query.get(id)
            db.session.delete(project)
            db.session.commit()
            interfaces = project.interface
            try:
                if interfaces:
                    for interface in interfaces:
                        db.session.delete(interface)
                        db.session.commit()
                    return jsonify({
                        'msg': '删除成功!',
                        'code': 200
                    })
                else:
                    return jsonify({
                        'code': 200,
                        'msg': '操作成功!'
                    })
            except Exception as e:
                return jsonify({
                    'code': 400,
                    'msg': e
                })

        except Exception as e:
            return jsonify({
                'code': 400,
                'msg': '操作失败!'
            })


class AddProjectApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            projectname = args.get('projectname')
            if projectname:
                project = Project(project_name=projectname)
                db.session.add(project)
                db.session.commit()
                return jsonify({
                    'code': 200,
                    'msg': '操作成功!'
                })
            else:
                return jsonify({
                    'code': 400,
                    'msg': '请输入项目名称!'
                })
        except Exception as e:
            return jsonify({
                'code': 400,
                'msg': '操作失败!'
            })


# @project.route('/getProjectDetail', methods=['POST', 'GET'])
# def getProjectDetail():
#     if request.method == 'GET':
#         projects = Project.query.filter(Project.is_delete == True).order_by(-Project.create_time).all()
#         return render_template('add/projectDetail.html', projects=projects)
#     else:
#         projectname = request.form.get('projectname')
#         if projectname:
#             project = Project.query.filter_by(project_name=projectname).all()
#             if not project:
#                 project = Project(project_name=projectname)
#                 db.session.add(project)
#                 db.session.commit()
#                 return render_template('add/projectDetail.html')
#             else:
#                 return render_template('add/projectDetail.html')
#         else:
#             pass
#
#
# @project.route('/searchProject', methods=['GET', 'POST'])
# def searchProject():
#     keyword = request.form.get('search')
#     if keyword:
#         projects = Project.query.filter(Project.project_name.contains(keyword)).all()
#         if len(projects) == 0:
#             return render_template('add/projectDetail.html', msg='暂无数据')
#         else:
#             return render_template('add/projectDetail.html', projects=projects)
#     else:
#         projects = Project.query.order_by(-Project.create_time).all()
#         return render_template('add/projectDetail.html', projects=projects)
#
#
# @project.route('/app/v1/editProject', methods=['GET', 'POST'])
# def editProject():
#     if request.method == 'POST':
#         try:
#             id = request.form.get('id')
#             project = Project.query.get(id)
#             projectname = request.form.get('projectname')
#             project.project_name = projectname
#             db.session.commit()
#             return redirect(url_for('user.getProjectDetail'))
#         except Exception as e:
#             return jsonify({'data': e.args[0], 'msg': '项目已存在'})
#     else:
#         id = request.args.get('id')
#         project = Project.query.get(id)
#         return render_template('update/update_project.html', project=project)
#
#
# @project.route('/deleteProject/<int:id>')
# def deleteProject(id):
#     # id = request.args.get('projectid')
#     project = Project.query.get(id)
#     project.is_delete = False
#     # db.session.delete(project)
#     db.session.commit()
#     return redirect(url_for('user.getProjectDetail'))


project_api.add_resource(AddProjectApi, '/addProject')
project_api.add_resource(GetProjectsApi, '/getProjects')
project_api.add_resource(GetProjectApi, '/getProject')
project_api.add_resource(UpdateProjectApi, '/updateProject')
project_api.add_resource(DeleteProjectApi, '/delete')
