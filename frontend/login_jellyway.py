import streamlit as st

# Hardcoded user credentials (you can replace this with a database or a more secure method)
valid_username = "admin"
valid_password = "password"

# Function to validate the login
def login(username, password):
    if username == valid_username and password == valid_password:
        return True
    return False

# Streamlit UI for the login page
def login_page():
    st.title("Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.success("Login successful!")
            st.write("Welcome, " + username + "!")
            # You can add more content or redirect here after successful login
        else:
            st.error("Invalid username or password")

# Main part of the app
if __name__ == "__main__":
    login_page()