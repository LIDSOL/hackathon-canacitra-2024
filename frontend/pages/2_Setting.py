import streamlit as st

st.set_page_config(
    page_title="JELLYWAY-Settings",
    page_icon="🗺️", # add icon
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

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
st.sidebar.header("Settings")

