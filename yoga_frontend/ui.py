import streamlit as st
from backend_api_client import show_user_classes,perform_login,perform_register_to_class,perform_registration,perform_search_by_day,perform_search_by_name,perform_search_by_time,perform_unregister_from_class

def main():
    st.title(f'Welcome to our Yoga Classes App!')
        
    col1, col2 = st.columns(2)
    col1.image("yoga_photo.jpg", width=300)

    initialize_session_state()

    if st.session_state.user_authenticated:
        show_search_options(col2)
        show_user_classes(col1)
    else:
        login_or_register(col2)

def initialize_session_state():
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""

def login_or_register(column):
    column.subheader("Login or Register")

    username = column.text_input("Enter your username:")
    password = column.text_input("Enter your password:", type="password")

    login_request = {"username": username, "password": password}

    if column.button("Login"):
        result = perform_login(login_request)
        if result:
            st.session_state.user_authenticated = True
            st.session_state.username = username
            st.success(f"Login successful for {st.session_state.username}!")
            st.rerun()
        else:
            st.warning("Login failed. Please try again.")
    if column.button("Register"):
        result = perform_registration(login_request)
        if result:
            st.info("Please log in to the website.")
    if st.session_state.user_authenticated:
        st.rerun()

def show_search_options(column):
    column.header("Search Classes")

    search_option = column.selectbox("Select search option:", ["By Day", "By Time", "By Name"])

    if search_option == "By Day":
        search_input = column.text_input("Enter the day:")
    elif search_option == "By Time":
        search_input = column.text_input("Enter the time of the day (morning\ afternoon\ evening):")
    else:
        search_input = column.text_input("Enter the class name:")

    if column.button("Search"):
        if search_input:
            if search_option == "By Day" or search_option == "By Time":
                search_input = search_input.lower()
                if search_option == "By Day":
                    st.session_state["result"+ search_option] = perform_search_by_day(search_input)
                else:
                    st.session_state["result"+ search_option] = perform_search_by_time(search_input)
            else:
                st.session_state["result"+ search_option] = perform_search_by_name(search_input)
    if column.button("Log out"):
        del st.session_state.user_authenticated
        st.session_state["resultBy Day"] = None
        st.session_state["resultBy Time"] = None
        st.session_state["resultBy Name"] = None
        st.rerun()

    display_classes(search_input, st.session_state.get("result"+search_option))

def display_classes(search_value, classes):
    st.subheader(f"Classes for {search_value}")
 
    if not classes:
        st.warning(f"No classes found for the selected {search_value}.")
        return

    for class_info in classes:
        st.write(f"Class information:\n"
                 f"Name: {class_info['classname']}\n"
                 f"Day: {class_info['day']}\n"
                 f"Time: {class_info['start_time']} - {class_info['end_time']}")
        
        register_button_key = f"register_button_{class_info['classname']}_{class_info['day']}_{class_info['start_time']}_{class_info['end_time']}"
        if st.button("Register", key=register_button_key):
            res=perform_register_to_class(class_info['classname'], class_info['day'], class_info['start_time'], class_info['end_time'], st.session_state.username)
            if "is already" in res:
                st.info(res)
            else:
                st.success(res)

        unregister_button_key = f"unregister_button_{class_info['classname']}_{class_info['day']}_{class_info['start_time']}_{class_info['end_time']}"
        if st.button("Unregister", key=unregister_button_key):
            res=perform_unregister_from_class(class_info['classname'], class_info['day'], class_info['start_time'], class_info['end_time'], st.session_state.username)
            if "is not registered" in res:
                st.info(res)
            else:
                st.success(res)

if __name__ == "__main__":
    main()

