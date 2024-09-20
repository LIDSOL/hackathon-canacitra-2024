import streamlit as st
import pandas as pd

# Import the custom curvy-style font using Google Fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&display=swap');
    h1 {
        font-family: 'Pacifico', cursive;
        font-size: 60pt;
        color: #A020F0;
        text-align: center;
    }
            


            w
    </style>
    """, unsafe_allow_html=True)

# Display your title with the custom font
st.markdown("<h1>JELLYWAY</h1>", unsafe_allow_html=True)