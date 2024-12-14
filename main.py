import os
import sys
import streamlit as st
from pathlib import Path
import page1,page2,page3
from streamlit_option_menu import option_menu



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
        
        st.sidebar.image(['/home/afif/Cao/Yolo-Streamlit/baterflai.jpg'], width=280,)
        with st.sidebar:
            app = option_menu(
                menu_title="BUTTERFLY",
                options=['IMAGE','VIDEO','URL LINKS'],   
                icons=['cloud-upload','compass','binoculars'],
                menu_icon='chat-text',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'#ff6666'},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "black"},
                    "nav-link-selected": {"background-color": "black"},}
                )  
        if app == "IMAGE":
            page1.app()
        if app == "VIDEO":
            page2.app()
        if app == "URL LINKS":
            page3.app()
    run()