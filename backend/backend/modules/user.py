from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from web import users as db_users
from web import clients as db_client
from web import redis_client
import uuid

class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        # Save user's session to Redis DB
        redis_client.set('user', str(session['user']))
        return jsonify(user), 200

    def signup(self):

        #Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "administrator": False
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing email address
        if db_users.find_one({ 
            "$or": [
                {"name": request.form.get('name')},
                {"email": request.form.get('email')}
                ] 
            }):
            return jsonify({ "error": "Email/Username address already in use" }), 400

        # Add User to db
        if db_users.insert_one(user):
            return self.start_session(user)

        return jsonify({ "error": "Singup failed" }), 400
    
    def signout(self):
        session.clear()
        redis_client.delete('user')
        return redirect('/')
    
    def login(self):
        user = db_users.find_one({
            "$or": [
                {"name": request.form.get('name')},
                {"email": request.form.get('name')}
            ]
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)
        
        return jsonify({ "error": "Invalid login credentials"}), 401
    

class UserAdmin(User):

    def __init__(self):
        super().__init__()

    def signup(self, name, email, password):

        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": name,
            "email": email,
            "password": password,
            "administrator": True  # Set administrator to True for UserAdmin
        }

        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Create Admin if not exist
        if not db_users.find_one({ 
            "$or": [
                {"name": name},
                {"email": email}
                ] 
            }):
            db_users.insert_one(user)

    def fetch_data(self):
        return list(db_client.find())
    
    def delete_record(self, id):
        db_client.delete_one({'_id': id})
        return redirect('/user/dashboard/admin/')
    
    def delete_record_all(self):
        if session['user']['administrator'] == True:
            db_client.delete_many({})
            return redirect('/user/dashboard/admin/')
        else:
            return jsonify({ "error": "Admin permission required"}), 401