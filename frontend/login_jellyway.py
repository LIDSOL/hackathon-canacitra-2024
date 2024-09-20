import streamlit as st

# Hardcoded user credentials (you can replace this with a database or a more secure method)
valid_username = "admin"
valid_password = "admin"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik+Spray+Paint&display=swap');
    
    h1 {
        text-align: center;
        color: #a822c9;
        font-family: "Rubik Spray Paint", system-ui;
        font-weight: 400;
        font-style: normal;
    }
    
    h2 {
        text-align: left;
        
    }
    </style>
    """, unsafe_allow_html=True)


def login(username, password):
    if username == valid_username and password == valid_password:
        return True
    return False

st.title("JELLY WAY")

def login_page():
    st.header("Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Button to handle login
    if st.button("Login"):
        if login(username, password):
            st.sidebar.success("Logged in!")
            st.write("Welcome, " + username + "!")
            st.session_state['page'] = 'main_page'
        else:
            st.error("Invalid username or password")
    
    # Button to redirect to "Forgot Password" page
    if st.button("Forgot Password"):
        st.session_state['page'] = 'forgot_password'

# Function to display the "Forgot Password" page
def forgot_password_page():
    st.title("Forgot Password")
    st.write("Please enter your email to reset your password.")
    
    email = st.text_input("Email")
    
    # Reset password button
    if st.button("Reset Password"):
        if email:
            st.success(f"Password reset instructions sent to {email}.")
        else:
            st.error("Please enter a valid email.")
    
    # Button to go back to the login page
    if st.button("Back to Login"):
        st.session_state['page'] = 'login'

# Main function to handle page switching
def main():
    # Set default page to login if session state doesn't exist
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    
    # Display the appropriate page based on session state
    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'forgot_password':
        forgot_password_page()

# Run the app
if __name__ == "__main__":
    main()
