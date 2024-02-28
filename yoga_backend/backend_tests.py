import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

user_login_data = {"username": "newuser", "password": "newpassword"}
not_exist_user_login={"username": "notexist", "password": "notexist"}
user_registration_data = {"username": "newuser", "password": "newpassword"}
class_name_data = {"name": "Classic Vinyasa Yoga  - IN-PERSON: Classic Vinyasa"}
day_of_week_data = {"day_of_the_week": "Monday"}
time_of_day_data = {"time_of_day": "morning"}
register_to_class_data =unregister_from_class_data = {
    "classname": "Classic Vinyasa Yoga  - IN-PERSON: Classic Vinyasa",
    "day": "Saturday, February 3",
    "starttime": "2:00 PM",
    "endtime": "3:15 PM",
    "username": "ayala",
}
user_registered_classes_data = {"username": "ayala"}

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "server is running!"}

@pytest.mark.skip(reason="Not a test")
def test_login_user_exist_endpoint():
    response = client.post("/v1/Login", json=user_login_data)
    assert response.status_code == 200
    assert "Login successful!" in response.json()["Message"]

def test_login_user_not_exist_endpoint():
    response = client.post("/v1/Login", json=not_exist_user_login)
    assert response.status_code == 200
    assert "You need to register to the website" in response.json()["Message"]

def test_register_endpoint():
    response = client.post("/v1/Register", json=user_registration_data)
    assert response.status_code == 200
    if "User registered successfully!" in response.json()["Message"]:
        assert "User registered successfully!" in response.json()["Message"]
    else:
        assert "Please choose a different username." in response.json()["Message"]

def test_find_classes_per_name_endpoint():
    response = client.post("/v1/ClassesPerName", json=class_name_data)
    assert response.status_code == 200
    expected_class_name = class_name_data["name"] 
    classes_info = response.json().get("Message", [])
    assert any(class_info["classname"] == expected_class_name for class_info in classes_info)

def test_find_classes_per_day_endpoint():
    response = client.post("/v1/ClassesPerDay", json=day_of_week_data)
    assert response.status_code == 200
    classes_info = response.json().get("Message", [])
    assert any("Monday" in class_info["day"] for class_info in classes_info)

def test_find_classes_per_time_endpoint():
    response = client.post("/v1/ClassesPertime", json=time_of_day_data)
    assert response.status_code == 200
    classes_info = response.json().get("Message", [])
    assert any("9:30 AM" in class_info["start_time"] for class_info in classes_info)

def test_register_to_class_endpoint():
    response = client.post("/v1/RegisterToClass", json=register_to_class_data)
    assert response.status_code == 200
    print(response.json()["Message"])
    assert "User ayala registered for class Classic Vinyasa Yoga  - IN-PERSON: Classic Vinyasa" in response.json()["Message"]

def test_unregister_from_class_endpoint():
    unregister_response = client.post("/v1/UnregisterFromClass", json=unregister_from_class_data)
    assert unregister_response.status_code == 200
    assert "User ayala unregistered from class Classic Vinyasa Yoga  - IN-PERSON: Classic Vinyasa" in unregister_response.json()["Message"]

def test_get_user_classes_endpoint():
    client.post("/v1/RegisterToClass", json=register_to_class_data)
    response = client.post("/v1/MyClasses", json=user_registered_classes_data)
    assert response.status_code == 200
    messages = response.json()["Message"]
    assert any("Classic Vinyasa Yoga  - IN-PERSON: Classic Vinyasa" in message["classname"] for message in messages)

@pytest.mark.parametrize(
    "endpoint, data",
    [
        ("/v1/Register", user_registration_data),
        ("/v1/Login", user_login_data), 
        ("/v1/Login", not_exist_user_login),
        ("/v1/ClassesPerName", class_name_data),
        ("/v1/ClassesPerDay", day_of_week_data),
        ("/v1/ClassesPertime", time_of_day_data),
        ("/v1/RegisterToClass", register_to_class_data),
        ("/v1/UnregisterFromClass", unregister_from_class_data),
        ("/v1/MyClasses", user_registered_classes_data),
    ],
)

def test_endpoints(endpoint, data):
    response = client.post(endpoint, json=data)
    assert response.status_code == 200
    assert "Message" in response.json()
