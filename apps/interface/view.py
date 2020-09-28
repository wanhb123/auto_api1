from flask import Blueprint, request, redirect, url_for, render_template

from apps.interface.models import Interface
from apps.project.models import Project
from ext import db

interface = Blueprint('interface', __name__, url_prefix='/interface')


@interface.route('/getInterfaceDetail')
def getInterfaceDetail():
    projects = Project.query.filter(Project.is_delete == True).all()
    interfaces = Interface.query.all()
    return render_template('add/InterfaceDetail.html', projects=projects, interfaces=interfaces)


@interface.route('/addInterface', methods=['GET', 'POST'])
def add_Interface():
    if request.method == 'POST':
        projectid = request.form.get('projectid')
        inf_name = request.form.get('interfacename')
        inf_url = request.form.get('url')
        req_method = request.form.get('reqmethod')
        req_parameter = request.form.get('parameter')
        interface = Interface(project_id=projectid, inf_url=inf_url, inf_name=inf_name, req_method=req_method,
                              req_parameters=req_parameter)
        db.session.add(interface)
        db.session.commit()
        return redirect(url_for('interface.getInterfaceDetail'))
    else:
        projects = Project.query.order_by(-Project.create_time).all()
        return render_template('add/addInterface.html', projects=projects)


@interface.route('/editInterface', methods=['GET', 'POST'])
def editInterface():
    if request.method == 'POST':
        id = request.form.get('id')
        interface = Interface.query.get(id)
        interface_name = request.form.get('interface_name')
        req_parameters = request.form.get('req_parameters')
        req_method = request.form.get('req_method')
        interface_url = request.form.get('url')
        interface.inf_name = interface_name
        interface.inf_url = interface_url
        interface.req_method = req_method.lower()
        interface.req_parameters = req_parameters
        if req_method == 'get' or req_method == 'post':
            db.session.commit()
            return redirect(url_for('user.getInterfaceDetail'))
        else:
            return render_template('update/update_interface.html', interface=interface, msg='不合法的请求方式')
    else:
        id = request.args.get('id')
        interface = Interface.query.get(id)
        return render_template('update/update_interface.html', interface=interface)


@interface.route('/deleteInterface/<int:id>')
def deleteInterface(id):
    interface = Interface.query.get(id)
    # interface.is_delete = False
    db.session.delete(interface)
    db.session.commit()
    return redirect(url_for('user.getInterfaceDetail'))


@interface.route('searchInterface', methods=['GET', 'POST'])
def searchInterface():
    keyword = request.form.get('search')
    if keyword:
        interfaces = Interface.query.filter(Interface.inf_name.contains(keyword)).all()
        if len(interfaces) == 0:
            return render_template('add/InterfaceDetail.html', msg='暂无数据')
        else:
            return render_template('add/InterfaceDetail.html', interfaces=interfaces)
    else:
        interfaces = Interface.query.all()
        return render_template('add/InterfaceDetail.html', interfaces=interfaces)
