from flask import Flask, request
from flask import jsonify, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.debug = True
bootstrap = Bootstrap(app)

user = {'username': 'Grey Li', 'bio': 'A boy who loves movies and music.'}

movies = [{'name': 'My Neighbor Totoro', 'year': '1988'}, {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'}, {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'}, {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'}, {'name': 'Gone Girl', 'year': '2014'}, {'name': 'CoCo', 'year': '2017'}]


@app.route('/index1', methods=['GET', 'POST'])
def index():
    name = 'flask'
    return render_template('/index.html', name=name)


@app.route('/get_request_info', methods=['post', 'get'])
def get_request_info():
    resp = dict()
    resp['headers'] = dict(request.headers)
    resp['params_data'] = dict(request.data)
    resp['params_form'] = dict(request.form)
    resp['params_query'] = dict(request.args)
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'post':
        name = request.form.get('name')
        print(name)
        return render_template('login.html', name=name)
    return render_template('login.html')


@app.route('/login')
def show():
    print('run!')


