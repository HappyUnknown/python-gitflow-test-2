db.getSiblingDB('admin');
db.auth(
    process.env.MONGO_INITDB_ROOT_USERNAME,
    process.env.MONGO_INITDB_ROOT_PASSWORD
);

db = db.getSiblingDB(process.env.MONGO_DB);

db.createUser({
    'user': process.env.MONGO_USER,
    'pwd': process.env.MONGO_PASSWORD,
    'roles': [{
        'role': 'dbOwner',
        'db': process.env.MONGO_DB
    }],
    "mechanisms" : [
        "SCRAM-SHA-1",
        "SCRAM-SHA-256"
    ]
});

db.createCollection('init');