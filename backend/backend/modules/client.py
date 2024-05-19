from flask import Flask, jsonify, request, session, redirect
from web import clients as db
from web import redis_client
from datetime import datetime
import uuid
import hashlib


class Client:

    def start_session(self, client):
        session['identify'] = True
        session['client'] = client
        # Save client session to Redis DB
        redis_client.set('client', str( session['client']))
        if client['status'] == 'declined':
            return redirect('/client/decline/dashboard/')
        if 'name' in client:
            return True
        return redirect('/client/updatedata/')
    
    def sesion_update(self):
        session['client'] = db.find_one({'_id': session['client']['_id'] })
        # Update client session in Redis DB
        redis_client.set('client', str(session['client']))

    def create_record(self, status):

        # Get client's IP addr
        client_ip = request.remote_addr
        # Hashing IP addr
        ip_hash = hashlib.sha256(client_ip.encode()).hexdigest()

        #Create the client object
        client = {
            "_id":      uuid.uuid4().hex,
            "status":   status,
            "ip":       client_ip,
            "ip_hash":  ip_hash
        }

        # Check for existing Client record
        if db.find_one({ "ip_hash": ip_hash }):
            return redirect('/client/dashboard')

        # Dell IP if declined
        if status == "declined":
            del client['ip']

        # Add Client to db
        if db.insert_one(client):
            return self.start_session(client)

        return jsonify(client), 200


    def client_accept(self):
        return self.create_record(status="accepted")

    def client_decline(self):
        return self.create_record(status="declined")
    
    def change_policy(self):
        updata = {
            'status': 'accepted',
            'ip':     request.remote_addr
        }
        db.update_one(
            {'_id': session['client']['_id']},
            {'$set': updata},
            upsert=False
        )
        self.sesion_update()
        return redirect('/client/updatedata/')

    def client_updata(self):
        # Set Time
        time = datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M")
        update_data = {
            'name': request.form.get('name'),
            'data': request.form.get('data'),
            'time': time
        }
        db.update_one(
            {'_id':  session['client']['_id']},
            {'$set': update_data},
            upsert=False
        )
        self.sesion_update()
        return jsonify(request.form)
    
    def check_if_decline(self):
        return session['client']['status'] == 'accepted'

    def client_exist(self):
        ip_hash = hashlib.sha256(request.remote_addr.encode()).hexdigest()
        client_data = db.find_one({'ip_hash': ip_hash})
        if client_data:
            return self.start_session(client_data)
        
    def fetch_data(self):
        require_fields = {'name': 1, 'data': 1, 'time': 1, '_id': 0}
        data_db = list(db.find({}, require_fields))
        return data_db

    def delete_record(self, id):
        db.delete_one({'_id': id})
        session.clear()
        redis_client.delete('client')
        return redirect('/')