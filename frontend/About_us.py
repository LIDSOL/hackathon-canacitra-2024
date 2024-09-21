import streamlit as st

st.set_page_config(
    page_title="JELLYWAY-About us",
    page_icon="assets/mi_icono.jpg",
    # layout="wide",
    menu_items={
        'Get Help': 'https://github.com/LIDSOL/hackathon-canacitra-2024',
        'Report a bug': "https://github.com/LIDSOL/hackathon-canacitra-2024",
        'About': "App that helps you find the best route to your destination in Mexico City."
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

st.markdown("## What is JELLY WAY?")
st.sidebar.header("Information")
st.write(
    """
### Your Companion in the Unexpected

Hello! We are a passionate team that understands that life is full of surprises. In Mexico, where climatic, geographical, and social events can change our plans in the blink of an eye, we are here to help you navigate those turbulent waters.

**Why is our app your best ally?**

🌟 **Always by Your Side**: We know that transportation can be a headache. Our goal is to ensure you never feel alone when facing the unexpected. With valuable, up-to-date information in real time, we keep you informed and prepared for any situation. You deserve to move without worries!

💰 **Save Time and Money**: Who doesn’t want to enjoy more free time? We help you find the fastest and most effective routes so you can focus on what really matters. Every second counts, and our app makes sure you make the most of them.

🤝 **Building Community**: You are not just a user; you are part of our family. Share your experiences and tips with other users who are also seeking solutions to the unexpected. Together, we are stronger and wiser.

🎨 **User-Friendly Design**: We’ve created an app that is as easy to use as a walk in the park. With an intuitive and appealing design, finding the information you need will be a piece of cake. No more complications!

**Ready to turn the unexpected into new opportunities?**
Download our app and join a community that supports one another. We are here to help you face any challenge with a smile. Let’s journey together towards tranquility!
"""
)