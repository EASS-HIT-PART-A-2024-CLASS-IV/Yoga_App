from fastapi import FastAPI,HTTPException
from backend_logic import user_registration,user_login,find_classes_per_name_of_the_class, find_classes_per_day_of_the_week, unregister_from_class, find_classes_per_time_of_the_day, register_to_class, get_user_classes
from models import ClassNameRequest,DayOfWeekRequest,TimeOfDayRequest,RegisterToClassRequest,UserLoginOrRegistrationRequest,UserRegisteredClassesRequest
app = FastAPI()

@app.get('/')
def root():
    return {"Message": "server is running!"}

@app.post('/v1/Login')
def login_endpoint(request: UserLoginOrRegistrationRequest):
    try:
       result = user_login(request.username,request.password)
       return {"Message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error")

@app.post('/v1/Register')
def register_endpoint(request: UserLoginOrRegistrationRequest):
    try:
        result = user_registration(request.username, request.password)
        return {"Message": result}
    except Exception as e:
        print(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Error")

@app.post('/v1/ClassesPerName')
def find_classes_per_name_endpoint(request: ClassNameRequest):
    try:
       result = find_classes_per_name_of_the_class(request.name)
       return {"Message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Don't find classes")

@app.post('/v1/ClassesPerDay')
def find_classes_per_day_endpoint(request: DayOfWeekRequest):
    try:
        result=find_classes_per_day_of_the_week(request.day_of_the_week)
        return {"Message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Don't find classes")

@app.post('/v1/ClassesPertime')
def find_classes_per_time_endpoint(request: TimeOfDayRequest):
    try:
        result=find_classes_per_time_of_the_day(request.time_of_day)
        return {"Message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Don't find classes")

@app.post('/v1/RegisterToClass')
def register_to_class_endpoint(request: RegisterToClassRequest):
    try:
        result_register=register_to_class(request.classname, request.day, request.starttime, request.endtime, request.username)
        return {"Message":result_register}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while register")

@app.post('/v1/UnregisterFromClass')
def unregister_from_class_endpoint(request: RegisterToClassRequest):
    try:
        result=unregister_from_class(request.classname, request.day, request.starttime, request.endtime, request.username)
        return {"Message":result}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error while unregister")

@app.post('/v1/MyClasses')
def get_user_classes_endpoint(request: UserRegisteredClassesRequest):
    try:
        classes =get_user_classes(request.username)
        return {"Message":classes}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Don't find classes")