from flask import Flask, render_template, url_for, request, redirect
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
import hashlib

############## Initialization ##############
app = Flask(__name__)
client = MongoClient("mongodb:27017")
#client = MongoClient('localhost', 27017)

# Mongodb database
db = client.flask_database
# Collection
clients = db.clients

######## Collection columns ########
# _id
# client_id
# status
# data
# ip_hash
######## Collection columns ########

############## Initialization ##############

@app.route("/", methods=['GET', 'POST'])
def index():
    # Get client's IP addr
    client_ip = request.remote_addr
    ip_hash = get_hash(client_ip)
    # Check if Client data exist
    client_data = ip_hash_exists(ip_hash)
    
    if request.method == 'POST':
        action = request.form.get('action')
        database_create(client_ip, action, ip_hash)
        if action == "yes":
            return redirect(url_for('form'))
        if action == "no":
            return redirect(url_for('declined'))
        if action == "update":
            return redirect(url_for('form'))
        if action == "delete":
            clients.delete_one({"ip_hash": ip_hash})
            return redirect(url_for('index'))
    return render_template('index.html', client_data=client_data)

@app.route("/form", methods=['GET', 'POST'])
def form():
    # Get client's IP addr
    client_ip = request.remote_addr
    ip_hash = get_hash(client_ip)
    # Get client's IP addr
    client_data = ip_hash_exists(ip_hash)
    if request.method == 'POST':
        data = request.form.get('data')
        database_update(ip_hash=ip_hash, data=data)
        return redirect(url_for('index'))
    all_data = clients.find()
    return render_template('form.html', client_ip=client_ip, clients=all_data, client_data=client_data)

@app.route("/declined", methods=['GET', 'POST'])
def declined():
    # Get client's IP addr
    client_ip = request.remote_addr
    ip_hash = get_hash(client_ip)
    if request.method == 'POST':
            action = request.form.get('action')
            if action == "delete":
                clients.delete_one({"ip_hash": ip_hash})
                return redirect(url_for('index'))
            if action == "accept":
                database_update(ip_hash, action=action, client_ip=client_ip)
                return redirect(url_for('form'))
    return render_template('declined.html')

# Get IP Hash
def get_hash(client_ip):
    # Hashing IP addr
    return hashlib.sha256(client_ip.encode()).hexdigest()

# Func to create record in database
def database_create(client_ip, action, ip_hash):
    # Get a value for client_id
    client_id = get_next_client_id()
    if action == 'yes':
        clients.insert_one({
            'client_id': client_id,
            'ip': client_ip, 
            'status': "accepted",
            'ip_hash': ip_hash 
            })
    elif action == 'no':
        clients.insert_one({
            'client_id': client_id,
            'status': "declined",
            'ip_hash': ip_hash 
            })
    
# Func to update database
def database_update(ip_hash, client_ip=None, data=None, action=None):
    update_data = {}
    if action:
        update_data['status'] = 'accepted'
    if client_ip:
        update_data['ip'] = client_ip
    if data:
        update_data['data'] = data
    
    if update_data:
        clients.update_one(
            {'ip_hash': ip_hash},
            {'$set': update_data},
            upsert=False  # Set to True if you want to create a new document when no document matches the query
        )

def ip_hash_exists(ip_hash):
    # Check if the client data already exist and return it
    client_data = clients.find_one({'ip_hash': ip_hash})
    return client_data

# Delete record
@app.post("/<id>/delete/")
def delete(id):
    clients.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('index'))

# Create counter collection for set unique client ID
def get_next_client_id():
    result = db.counters.find_one_and_update(
        {'_id': 'client_id'},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return result['seq']

# Run web-server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

