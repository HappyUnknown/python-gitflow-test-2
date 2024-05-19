from flask import Flask
from web import app
from modules.user import User, UserAdmin
from modules.client import Client

############ Users Route ############

@app.route('/user/signup', methods=['POST'])
def sign_up():
  return User().signup()

@app.route('/user/signout')
def sign_out():
  return User().signout()

@app.route('/user/login', methods=['POST'])
def log_in():
  return User().login()

@app.route('/user/admin/delete/<id>')
def admin_delete_record(id):
  return UserAdmin().delete_record(id)

@app.route('/user/admin/delete_all')
def admin_delete_record_all():
  return UserAdmin().delete_record_all()

############ Clients Route ############

@app.route('/client/decline')
def decline():
  return Client().client_decline()

@app.route('/client/accept')
def accept():
  return Client().client_accept()

@app.route('/client/delete/<id>')
def client_delete(id):
  return Client().delete_record(id)

@app.route('/client/updata', methods=['POST'])
def client_updata():
  return Client().client_updata()

@app.route('/client/change_policy')
def change_policy():
  return Client().change_policy()