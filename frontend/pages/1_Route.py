import streamlit as st

# Hardcoded user credentials (you can replace this with a database or a more secure method)
valid_email = "admin"
valid_password = "admin"

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# Set page configuration
st.set_page_config(
    page_title="JELLYWAY-Map",
    page_icon="🗺️", # add icon
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik+Spray+Paint&display=swap');
    
    h1 {
        text-align: center;
        color: #a822c9;
        font-family: "Rubik Spray Paint", system-ui;
        font-size: 60px;
        font-weight: 400;
        font-style: normal;
    }
    
    h2 {
        text-align: left;
        font_size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("# JELLYWAY")
st.sidebar.header("Map")

def login(username, password):
    if username == valid_email and password == valid_password:
        return True
    return False

def login_page():
    st.markdown("## Login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Button to handle login
    if st.button("Login"):
        if login(email, password):
            st.success("Logged in! Welcome, " + email + "!")
            st.session_state['logged_in'] = True
            st.session_state['page'] = 'route_page'
        else:
            st.error("Invalid username or password")
    
    # Button to redirect to "Forgot Password" page
    if st.button("Forgot Password"):
        st.session_state['page'] = 'forgot_password'

# Function to display the "Forgot Password" page
def forgot_password_page():
    st.markdown("## Forgot Password")
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

# Function to display the main page after logging in
def route_page():
    st.markdown("## Route")
    st.write("This is the main page after logging in.")

    # Button to log out
    if st.button("Log Out"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'login'

# Main logic to control page display
if st.session_state['logged_in']:
    route_page()
else:
    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'forgot_password':
        forgot_password_page()