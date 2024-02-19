from pydantic import BaseModel

class UserLoginOrRegistrationRequest(BaseModel):
    username: str
    password: str

class ClassNameRequest(BaseModel):
    name: str

class DayOfWeekRequest(BaseModel):
    day_of_the_week: str

class TimeOfDayRequest(BaseModel):
    time_of_day: str

class RegisterToClassRequest(BaseModel):
    classname: str
    day: str
    starttime: str
    endtime: str
    username: str

class UserRegisteredClassesRequest(BaseModel):
    username: str