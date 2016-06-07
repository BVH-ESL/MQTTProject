from pymongo import MongoClient
client = MongoClient()
db = client.mqtt
# print db    
cursor = db.device.find()
#print(cursor)
for document in cursor:
    print(document)
