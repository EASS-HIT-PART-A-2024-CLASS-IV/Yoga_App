import streamlit as st
import httpx

backend_base_url = "http://backend:8001"

def perform_login(login_request):
    api_url = f"{backend_base_url}/v1/Login"
    try:
        response = httpx.post(api_url, json=login_request)
        response.raise_for_status()
        result = response.json()["Message"]
        return "Login successful!" in result
    except httpx.RequestError as e:
        st.error(f"Error during login request: {e}")
        return False
    except httpx.HTTPStatusError as e:
        st.error(f"HTTP error during login request: {e}")
        return False
    
def perform_registration(login_request):
    api_url = f"{backend_base_url}/v1/Register"
    try:
        response = httpx.post(api_url, json=login_request)
        response.raise_for_status()
        result = response.json()["Message"]

        if "User registered successfully!" in result:
            st.success(f"Registration successful for {login_request['username']}!")
            return True
        else:
            st.warning("Registration failed. Please choose a different username.")
            return False
    except httpx.RequestError as e:
        st.error(f"Error during registration request: {e}")
        return False
    except httpx.HTTPStatusError as e:
        st.error(f"HTTP error during registration request: {e}")
        return False
    
def perform_search_by_day(day_of_the_week):
    api_url = f"{backend_base_url}/v1/ClassesPerDay"
    data = {"day_of_the_week": day_of_the_week}
    try:
        response = httpx.post(api_url, json=data)
        response.raise_for_status()
        result = response.json()["Message"]
        return result
    except httpx.RequestError as e:
        return f"Error during request: {e}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error during request: {e}"
    
def perform_search_by_time(time_of_day):
    api_url = f"{backend_base_url}/v1/ClassesPertime"
    data = {"time_of_day": time_of_day}
    try:
        response = httpx.post(api_url, json=data)
        response.raise_for_status()
        result = response.json()["Message"]
        return result
    except httpx.RequestError as e:
        return f"Error during request: {e}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error during request: {e}"

def perform_search_by_name(class_name):
    api_url = f"{backend_base_url}/v1/ClassesPerName"
    data = {"name": class_name}
    try:
        response = httpx.post(api_url, json=data)
        response.raise_for_status()
        result = response.json()["Message"]
        return result
    except httpx.RequestError as e:
        return f"Error during request: {e}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error during request: {e}"

def show_user_classes(column):
    try:
        api_url = f"{backend_base_url}/v1/MyClasses"
        data = {"username": st.session_state.username}

        response = httpx.post(api_url, json=data)
        response.raise_for_status()
        user_classes = response.json()["Message"]

        if user_classes:
            column.subheader("Your Classes")
            for class_info in user_classes:
                column.write(
                    f"**{class_info['classname']}**\n"
                    f"Day: {class_info['day']}\n"
                    f"Time: {class_info['start_time']} - {class_info['end_time']}\n"
                )
        else:
            column.warning("You are not registered for any classes.")
    except httpx.RequestError as e:
        column.error("Error getting user classes. Please try again.")
    except httpx.HTTPStatusError as e:
        column.error("Error getting user classes. Please try again.")

def perform_register_to_class(classname, day, starttime, endtime, username):
    api_url = f"{backend_base_url}/v1/RegisterToClass"
    data = {
        "classname": classname,
        "day": day,
        "starttime": starttime,
        "endtime": endtime,
        "username": username
    }
    try:
        response = httpx.post(api_url, json=data)
        response.raise_for_status()
        result = response.json()["Message"]
        return result

    except httpx.RequestError as e:
        return f"Error during request to {api_url}: {e}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error during request to {api_url}: {e}"
    except Exception as e:
        return f"Unexpected error during request: {e}"

def perform_unregister_from_class(classname, day, starttime, endtime, username):
    api_url = f"{backend_base_url}/v1/UnregisterFromClass"
    data = {
        "classname": classname,
        "day": day,
        "starttime": starttime,
        "endtime": endtime,
        "username": username
    }

    try:
        response = httpx.post(api_url, json=data)
        response.raise_for_status()
        result = response.json()["Message"]
        return result

    except httpx.RequestError as e:
        return f"Error during request: {e}"
    except httpx.HTTPStatusError as e:
        return f"HTTP error during request: {e}"
    except Exception as e:
        return f"Unexpected error during request: {e}"