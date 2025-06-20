
import os
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import base64
import subprocess
# Function to get base64 encoding of a file
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set the background of the Streamlit app
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpeg;base64,%s");
    background-position: center;
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(
        """
        <style>
            h1 {
                color: black;
                font-family: 'Times New Roman', serif;
                font-weight: bold;
            }
            p {
                color: green;
                font-family: 'Times New Roman', serif;
                font-weight: bold;
            }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('background/3.jpg')

# Streamlit app title
st.title(" OVERWATCH-APT Threat Detection")


import streamlit as st
import sqlite3
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to create the SQLite database
def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# Call the function to create the database
create_db()

# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Function to authenticate a user
def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None



# Sidebar for authentication options
option = st.sidebar.selectbox("Choose an option", ["Login", "Register"])

if option == "Register":
    st.header("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(username, password):
            st.success("Registration successful!")
        else:
            st.error("Username already exists.")
            
elif option == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful!")
            subprocess.run(["streamlit", "run", "app1.py"]) 
            
            # Voice command section after login
            recognizer = sr.Recognizer()

            def listen():
                with sr.Microphone() as source:
                    st.write("Listening...")
                    audio = recognizer.listen(source)
                    try:
                        text = recognizer.recognize_google(audio)
                        st.write(f"Recognized: {text}")
                        return text
                    except sr.UnknownValueError:
                        st.write("Sorry, I did not understand that.")
                        return None
                    except sr.RequestError:
                        st.write("Sorry, there was an error with the speech recognition service.")
                        return None

        else:
            st.error("Invalid username or password.")
