from pymongo import MongoClient
from datetime import datetime
import re

client = MongoClient("mongodb://ayalat:Aa123456@yoga_mongodb2:27017")

dbname="YogaDB"
database = client[dbname]
collection_classes = database["YogaClass"]
collection_users = database["Users"]

def user_login(username, password):
    user_data = collection_users.find_one({"username": username})
    if user_data:
        if user_data["password"] == password:
            return "Login successful!"
        else:
            return "Incorrect password"
    else:
        return "You need to register to the website"

def user_registration(username, password):
    existing_user = collection_users.find_one({"username": username})
    if existing_user:
        return "Please choose a different username."
    else:
        new_user = {
            "username": username,
            "password": password,
        }
        collection_users.insert_one(new_user)
        return "User registered successfully!"

def find_classes_per_name_of_the_class(name):
    result_class_per_name = []
    for element in collection_classes.find({"classname": name}):
        element['_id'] = str(element['_id'])
        result_class_per_name.append(element)
    return result_class_per_name

def find_classes_per_day_of_the_week(day_of_the_week):
    result_class_per_day = []
    regex_pattern = re.compile(f"{day_of_the_week}", re.IGNORECASE)
    for element in collection_classes.find({"day": {"$regex": regex_pattern}}):
        element['_id'] = str(element['_id'])
        result_class_per_day.append(element)
    return result_class_per_day

def find_classes_per_time_of_the_day(time_of_day):
    start_hour, end_hour = None, None
    result_class_per_time = []

    if time_of_day.lower() == "morning":
        start_hour, end_hour = 6, 12
    elif time_of_day.lower() == "afternoon":
        start_hour, end_hour = 12, 18
    elif time_of_day.lower() == "evening":
        start_hour, end_hour = 18, 23
    if start_hour is not None and end_hour is not None:
        for element in collection_classes.find():
            class_start_time = datetime.strptime(element["start_time"], "%I:%M %p").time()
            class_end_time = datetime.strptime(element["end_time"], "%I:%M %p").time()
            if start_hour <= class_start_time.hour < end_hour or \
                    start_hour <= class_end_time.hour <= end_hour:
                element['_id'] = str(element['_id'])
                result_class_per_time.append(element)
    return result_class_per_time

def register_to_class(classname, day, starttime, endtime, username):
    class_document = collection_classes.find_one({
        "classname": classname,
        "day": day,
        "start_time": starttime,
        "end_time": endtime
    })

    if class_document:
        user_document = collection_users.find_one({"username": username})
        if user_document:
            if "myclasses" not in user_document:
                user_document["myclasses"] = []

            if class_document["_id"] not in user_document["myclasses"]:
                user_document["myclasses"].append(class_document["_id"])

                collection_users.update_one(
                    {"_id": user_document["_id"]},
                    {"$set": {"myclasses": user_document["myclasses"]}}
                )

                return f"User {username} registered for class {classname} on {day} from {starttime} to {endtime}."
            else:
                return f"User {username} is already registered for class {classname}."
        else:
            return "User not found"
    else:
        return "Class not found"

def unregister_from_class(classname, day, starttime, endtime, username):
    class_document = collection_classes.find_one({
        "classname": classname,
        "day": day,
        "start_time": starttime,
        "end_time": endtime
    })

    if class_document:
        user_document = collection_users.find_one({"username": username})
        if user_document:
            if "myclasses" in user_document and class_document["_id"] in user_document["myclasses"]:
                user_document["myclasses"].remove(class_document["_id"])

                collection_users.update_one(
                    {"_id": user_document["_id"]},
                    {"$set": {"myclasses": user_document["myclasses"]}}
                )

                return f"User {username} unregistered from class {classname} on {day} from {starttime} to {endtime}."
            else:
                return f"User {username} is not registered for class {classname}."
        else:
            return "User not found."
    else:
        return "Class not found."
     
def get_user_classes(username):
    user_data = collection_users.find_one({"username": username})
    if user_data:
        if "myclasses" in user_data:
            class_ids = user_data["myclasses"]
            registered_classes = []
            for id in class_ids:
                class_data = collection_classes.find_one({"_id": id})
                if class_data:
                    class_data['_id'] = str(class_data['_id'])
                    registered_classes.append(class_data)
                else:
                    return f"Class with ID {id} not found"
            return registered_classes
        else:
            return []