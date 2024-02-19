from pymongo import MongoClient
import json
import os

json_file_path = os.environ.get("JSON_FILE_PATH", "/app/yoga_db/yoga_data.json")

client = MongoClient("mongodb://ayalat:Aa123456@yoga_mongodb2:27017")

dbname="YogaDB"

database = client[dbname]
collection = database["Users"]

user_data = [
    {"username": "ayala", "password": "1235464ww"},
    {"username": "nir", "password": "ekjej47587"},
    {"username": "ron", "password": "dwjdwklj133"}
]

collection.insert_many(user_data)

collection = database["YogaClass"]
collection.delete_many({})
with open(json_file_path, "r") as json_file:
    class_details_list = json.load(json_file)

for class_details in class_details_list:
    collection.insert_one({
        "classname": class_details["classname"],
        "day": class_details["day"],
        "start_time": class_details["start_time"],
        "end_time": class_details["end_time"]
    })

client.close()
