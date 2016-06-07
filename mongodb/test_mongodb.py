from pymongo import MongoClient
client = MongoClient()
#client = MongoClient("mongodb://192.168.1.181:27019")
db = client.test
cursor = db.restaurants.find({"borough": "Manhattan"})
#print(cursor)
for document in cursor:
    print(document)
