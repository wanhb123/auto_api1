import re

from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, fields, marshal_with, reqparse

from apps.user.models import User
from apps.utils.createDate import CreateDate
from ext import db

user_api = Blueprint('user', __name__, url_prefix='/user')
api = Api(user_api)

user_fields = {
    'id': fields.String(default=''),
    'username': fields.String(default=''),
    'email': fields.String(default=''),
    'phone': fields.String(default=''),
    'createtime': CreateDate(dt_format='strftime', default='')
}

resource_fields = {
    'code': fields.Integer,
    'msg': fields.String,
    'data': fields.List(fields.Nested(user_fields), default=[]),
    'total': fields.Integer
}
users_parser = reqparse.RequestParser()
users_parser.add_argument('search', help='', location=['json', 'args'], type=str)
users_parser.add_argument('page', help='当前页码不能为空', location=['json', 'args'], type=int, required=True)
users_parser.add_argument('size', help='当前页显示用户数量不能为空', location=['json', 'args'], type=int, required=True)

class UserApi(Resource):
    @marshal_with(resource_fields)
    def post(self):
        try:
            args = users_parser.parse_args()
            page = args.get('page')
            size = args.get('size')
            keyword = args.get('search')
            if not keyword:
                users = User.query.order_by(User.createtime.desc()).limit(size).offset((page - 1) * size)
                total = User.query.count()
            else:
                users = User.query.filter(User.username.contains(keyword)).limit(size).offset((page - 1) * size)
                total = User.query.filter(User.username.contains(keyword)).count()
        except Exception as e:
            return {
                'code': 0,
                'msg': e,
                'data': '',
                'total': 0
            }
        return {
            'code': 200,
            'msg': '操作成功',
            'data': users,
            'total': total
        }


user_parser = reqparse.RequestParser()
user_parser.add_argument('id', help='用户id不能为空', location=['json', 'args'], type=int, required=True)


class UserDeleteApi(Resource):
    def post(self):
        try:
            args = user_parser.parse_args()
            id = args.get('id')
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return jsonify({
                'code': 200,
                'msg': '删除成功',
            })
        except Exception as e:
            return jsonify({
                'code': 404,
                'msg': e,
            })


class UserAddApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            name = args.get('data').get('name')
            password = args.get('data').get('password')
            repassword = args.get('data').get('repassword')
            phone = args.get('data').get('phone')
            email = args.get('data').get('email')
            get_phone = User.query.filter(User.phone == phone).first()
            ret = re.match('1[3-9]\d{9}', phone)
            if ret:
                if password == repassword:
                    if not get_phone:
                        user = User(username=name, password=password, phone=ret.group(), email=email)
                        db.session.add(user)
                        db.session.commit()
                    else:
                        return jsonify({'msg': '手机号码已存在!'})
                else:
                    return jsonify({'msg': '两次密码输入不一致!'})
            else:
                return jsonify({
                    'code': 400,
                    'msg': '请输入合法的手机号码！'
                })
        except Exception as e:
            return jsonify({'code': 404, 'msg': '操作失败!'})
        return jsonify({'code': 200, 'msg': '操作成功!'})

class GetUserApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            id = data.get('id')
            user = User.query.filter(User.id == id).first()
            return jsonify({
                'code': 200,
                'msg': '操作成功!',
                'data': {
                    'name': user.username,
                    'email': user.email,
                    'phone': user.phone,
                }})
        except Exception as e:
            return jsonify({
                'code': 405,
                'msg': e,
            })


edit_parser = reqparse.RequestParser()
edit_parser.add_argument('id', help='', type=int, location='form')


class UserEditApi(Resource):
    def post(self):
        try:
            args = request.get_json()
            id = args.get('id')
            name = args.get('name')
            email = args.get('email')
            phone = args.get('phone')
            user = User.query.filter(User.id == id).first()
            get_phone = User.query.filter(User.phone == phone).first()
            ret = re.match('1[3-9]\d{9}', phone)
            if ret:
                if not get_phone or phone == user.phone:
                    try:
                        user.username = name
                        user.phone = ret.group()
                        user.email = email
                        db.session.commit()
                        return jsonify({'code': 200, 'msg': '操作成功!'})
                    except Exception as e:
                        return jsonify({
                            'msg': '操作失败!'
                        })
                else:
                    return jsonify({
                        'msg': '手机号码已存在!'
                    })
            else:
                return jsonify({
                    "code": 400,
                    'msg': '请输入正确的手机号!'
                })
        except Exception as e:
            return jsonify({
                'code': 400,
                'msg': e,
            })

class LoginApi(Resource):
    def post(self):
        data = request.get_json()
        phone = data.get('phone')
        password = data.get('password')
        if phone and password:
            try:
                user = User.query.filter(User.phone == phone).first()
                if user:
                    if user.password == password:
                        return jsonify({
                            'code': 200,
                            'msg': '操作成功!',
                            'username': user.username,
                        })
                    else:
                        return jsonify({
                            'code': 400,
                            'msg': '用户名或密码错误，请重新输入。'
                        })
                else:
                    return jsonify({
                        'code': 400,
                        'msg': '用户不存在!'
                    })
            except Exception as e:
                return jsonify({
                    'code': 400,
                    'msg': str(e),
                })
        else:
            return jsonify({
                'code': 400,
                'msg': '请输入正确的用户名或密码!'
            })


api.add_resource(UserApi, '/users')
api.add_resource(GetUserApi, '/user')
api.add_resource(UserDeleteApi, '/delete')
api.add_resource(UserAddApi, '/add')
api.add_resource(UserEditApi, '/edit')
api.add_resource(LoginApi, '/login')
