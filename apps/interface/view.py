import requests
from flask import Blueprint, request, jsonify
from flask_restful import Resource, Api, fields, marshal_with

from apps.interface.models import Interface
from apps.project.models import Project
from apps.utils.createDate import CreateDate
from ext import db

interface = Blueprint('interface', __name__, url_prefix='/interface')
interface_api = Api(interface)

interface_fields = {
    'id': fields.String(default=''),
    'interfacename': fields.String(default='', attribute='inf_name'),
    'interfaceurl': fields.String(default='', attribute='inf_url'),
    'type': fields.String(default='', attribute='req_method'),
    'createtime': CreateDate(dt_format='strftime', default='', attribute='create_time'),
    'parames': fields.String(default='', attribute='req_parameters'),
    'createperson': fields.String(default='', attribute='create_person'),
    'project': fields.String(default=''),
}

resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(interface_fields), default=[]),
    'total': fields.Integer
}


class GetInterfaceApi(Resource):
    @marshal_with(resource_fields)
    def post(self):
        try:
            args = request.get_json()
            page = args.get('page')
            size = args.get('size')
            keyword = args.get('search')
            id = args.get('projectid')
            if not keyword:
                if id:
                    project = Project.query.filter(Project.id == id).first()
                    interfaces = project.interface
                    total = len(interfaces)
                    return ({
                        'code': 200,
                        'msg': '操作成功!',
                        'data': interfaces,
                        'total': total
                    })
                else:
                    pagination = Interface.query.order_by(Interface.create_time.desc()).paginate(page=page,
                                                                                                 per_page=size)
                    interface = pagination.items
                    total = Interface.query.count()
            else:
                pagination = Interface.query.filter(Interface.inf_name.contains(keyword)).paginate(page, size)
                interface = pagination.items
                total = Interface.query.filter(Interface.inf_name.contains(keyword)).count()
            return ({
                'code': 200,
                'msg': '操作成功!',
                'data': interface,
                'total': total
            })
        except Exception as e:
            return ({
                'code': 400,
                'msg': '操作失败!',
                'data': [],
                'total': 0
            })


class AddInterfaceApi(Resource):
    def post(self):
        args = request.get_json()
        name = args.get('data').get('name')
        project = args.get('data').get('project')
        url = args.get('data').get('url')
        type = args.get('data').get('type')
        parames = args.get('data').get('parames')
        createperson = args.get('data').get('createperson')
        interface = Interface(inf_name=name, inf_url=url, req_method=type, req_parameters=parames, project_id=project,
                              create_person=createperson)
        db.session.add(interface)
        db.session.commit()
        return jsonify({
            'code': 200,
            'msg': '操作成功!'
        })


class QueryProjectsApi(Resource):
    def post(self):
        try:
            projects = Project.query.all()
            lis = []
            for project in projects:
                dic = {}
                dic['id'] = project.id
                dic['name'] = project.project_name
                lis.append(dic)
            return jsonify({
                'msg': '操作成功!',
                'code': 200,
                'data': lis
            })
        except Exception as e:
            return jsonify({
                'code': 400,
                'msg': '操作失败!'
            })


class DeleteInterfaceApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            id = args.get('id')
            interface = Interface.query.get(id)
            db.session.delete(interface)
            db.session.commit()
        except Exception as e:
            return jsonify({
                'code': 400,
                'msg': '操作失败!'
            })
        return jsonify({
            'code': 200,
            'msg': '操作成功!'
        })


class UpdateInterfaceApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            id = args.get('data').get('id')
            name = args.get('data').get('name')
            query_interface = Interface.query.get(id)
            project_id = args.get('data').get('project')
            req_type = args.get('data').get('type')
            parames = args.get('data').get('parames')
            url = args.get('data').get('url')
            query_interface.inf_name = name
            query_interface.inf_url = url
            query_interface.req_method = req_type
            query_interface.req_parameters = parames
            query_interface.project_id = project_id
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


class QueryInterfaceApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            id = args.get('id')
            get_interface = Interface.query.get(id)
            project = get_interface.project.id
            return jsonify({
                'code': 200,
                'msg': '操作成功!',
                'data': {
                    'url': get_interface.inf_url,
                    'parames': get_interface.req_parameters,
                    'name': get_interface.inf_name,
                    'type': get_interface.req_method,
                    'project': project
                }
            })
        except Exception as e:
            return jsonify({
                'code': 400,
                'msg': e,
            })


class ExeRequestInterfaceApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            id = args.get('id')
            id = id[0]
            query_interface = Interface.query.get(id)
            req_type = query_interface.req_method
            parames = query_interface.req_parameters.encode('utf-8')
            url = query_interface.inf_url
            if req_type == 'post':
                res = requests.post(url, data=parames)
            else:
                res = requests.get(url)
            return jsonify({
                'code': 200,
                'msg': '操作成功!',
                'res': res.text
            })
        except Exception as e:
            return jsonify({
                'code': 400,
                'msg': '操作失败,请检查相应的信息输入是否正确!'
            })


interface_api.add_resource(GetInterfaceApi, '/interfaces')
interface_api.add_resource(AddInterfaceApi, '/addinterface')
interface_api.add_resource(QueryProjectsApi, '/queryProjects')
interface_api.add_resource(DeleteInterfaceApi, '/deleteInterface')
interface_api.add_resource(UpdateInterfaceApi, '/updateInterface')
interface_api.add_resource(QueryInterfaceApi, '/getInterface')
interface_api.add_resource(ExeRequestInterfaceApi, '/requestInterfaces')
