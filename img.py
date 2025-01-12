import streamlit as st
from ultralytics import YOLO
import PIL

def text_detection(file):
    model = YOLO("rama.pt")
    uploaded_image = PIL.Image.open(file)
    res = model.predict(uploaded_image,conf=0.5,save=False)
    box = res[0].boxes.xyxy.tolist()
    res_plotted = res[0].plot()[:, :, ::-1]
    st.image(res_plotted, caption='Text Detections',use_column_width=True)
    st.write("Number of the Detections : "+str(len(box)))
    return uploaded_image

def app(conf, model):
    st.title("Butterfly Detection on Image Input") 
    source_img = None
    source_img = st.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)
    with col1:
        try:
            if source_img is None:
                st.write("No image chosen")
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)
    with col2:
        if st.sidebar.button('Detect'):
            uploaded_image = PIL.Image.open(source_img)
            res = model.predict(uploaded_image,conf=0.5,save=False)
            box = res[0].boxes.xyxy.tolist()
            res_plotted = res[0].plot()[:, :, ::-1]
            st.image(res_plotted, caption='Text Detections',use_column_width=True)
            st.write("Number of the Detections : "+str(len(box)))