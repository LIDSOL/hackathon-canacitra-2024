import streamlit as st
import hashlib

# Hardcoded user credentials (you can replace this with a database or a more secure method)
valid_email = "admin"
valid_password = "password"

# Function to validate the login
def login(email, password):
    if email == valid_email and password == valid_password:
        return True
    return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    st.title("Login Page")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    hashed_password = hash_password(password)


    if st.button("Login"):
        if login(email, password):
            st.success("Login successful!")
            st.write("Welcome, "+ email +"!")
            # You can add more content or redirect here after successful login
        else:
            st.error("Invalid Email or password")

# Main part of the app
if __name__ == "__main__":
    login_page()