from flask import Flask, render_template, session, redirect, request
from pymongo import MongoClient
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.middleware.proxy_fix import ProxyFix
from functools import wraps
import os
import redis

############## Initialization ##############

app = Flask(__name__)

app.secret_key = b'\x9d\x18\x8bH`\x03\xae\x00\xf3L\xd3\xaf\x06\xc8\x9a\x92'
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Map variables
for variable, value in os.environ.items():
    if variable.startswith("MONGO_"):
        env_name = variable.split("MONGO_")[1]
        app.config[env_name] = value
        print(env_name)

# Local DB for Development
# client = MongoClient('localhost', 27017)

# Connect to Mongo
client = MongoClient('mongodb', username=app.config['USER'], password=app.config['PASSWORD'], authSource='flask_database', authMechanism='SCRAM-SHA-256')

# Initialize Redis client
redis_client = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True, db=0)

# Database
db = client.flask_database

# Collection
users = db.users
clients = db.clients

############## Swagger ##############
SWAGGER_URL = '/docs'  # URL route for Swagger UI
API_URL = '/static/swagger.json'  # Our API url (local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "MongoDB Flask App"
    },
)
app.register_blueprint(swaggerui_blueprint)


############## Decorators ##############
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwardgs):
        if 'logged_in' in session:
            return f(*args, **kwardgs)
        else:
            return redirect('/')
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwardgs):
        if session['user']["administrator"] == True:
            return redirect('/user/dashboard/admin/')
        else:
            return f(*args, **kwardgs)
    return wrap

def identify_required(f):
    @wraps(f)
    def wrap(*args, **kwardgs):
        if 'identify' in session:
            return f(*args, **kwardgs)
        else:
            return redirect('/')
    return wrap

def clinet_declined(f):
    @wraps(f)
    def wrap(*args, **kwardgs):
        if session['client']['status'] == 'declined':
            return redirect('/client/decline/dashboard/')
        else:
            return f(*args, **kwardgs)
    return wrap

############## Modules ##############
from modules import routes
from modules.client import Client
from modules.user import UserAdmin

# Create Admin acount
UserAdmin().signup(name=app.config['ADMIN_USER'], email=app.config['ADMIN_EMAIL'], password=app.config['ADMIN_PASS'])

@app.route('/')
def home():
    if Client().client_exist():
        return redirect('/client/dashboard')
    return render_template('home.html')

############## Users HTML ##############

@app.route('/user/dashboard/')
@admin_required
def dashboard():
    data_db = Client().fetch_data()
    return render_template('user/dashboard.html', data_db=data_db)

@app.route('/user/dashboard/admin/')
@login_required
def client_dashboard_admin():
    data_db = UserAdmin().fetch_data()
    return render_template('user/dashboard_admin.html', data_db=data_db)

@app.route('/user/login/')
def login():
    return render_template('user/login.html')

@app.route('/user/registry/')
def registry():
    return render_template('user/registry.html')

############## Clients HTML ##############

@app.route('/client/dashboard/')
@clinet_declined
@identify_required
def client_dashboard():
    data_db = Client().fetch_data()
    return render_template('client/dashboard.html', data_db=data_db )

@app.route('/client/updatedata/')
@clinet_declined
@identify_required
def client_update_data():
    return render_template('client/update.html')

@app.route('/client/decline/dashboard/')
@identify_required
def client_dashboard_decline():
    if Client().check_if_decline():
        return redirect('/client/dashboard')
    return render_template('client/dashboard_decline.html')
