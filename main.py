import os
import sys
import streamlit as st
from pathlib import Path
import img,vid
from streamlit_option_menu import option_menu
from ultralytics import YOLO

st.set_page_config(
    page_title="GROUP 5",
    layout="wide"
)


class MultiApp:
    def __init__(self):
        self.apps = []
        
    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })
        
    def run():
        model = YOLO("rama.pt")
    
        st.sidebar.image(['baterflai.jpg'], width=280,)
        with st.sidebar:
            app = option_menu(
                menu_title="Baterplai",
                options=['Image','Video','URL Link'],   
                icons=['cloud-upload','film','globe'],
                menu_icon='bootstrap',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'#ff6666',"font":"serif"},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "black"},
                    "nav-link-selected": {"background-color": "black"},}
                )         
            confidence = float(st.sidebar.slider(
            "Select Model Confidence", 25, 100, 40)) / 100   
        if app == "Image":
            img.app(confidence, model)
        if app == "Video":
            vid.play_stored_video(confidence, model)
        if app == "URL Link":
            vid.play_youtube_video(confidence,model)        
    run()