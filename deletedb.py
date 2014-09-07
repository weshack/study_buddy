from pymongo import MongoClient
client=MongoClient()
db=client.sbdb
db.drop_collection('users')
db.drop_collection('group_sessions')
