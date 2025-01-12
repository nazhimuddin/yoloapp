from ultralytics import YOLO
import streamlit as st
import cv2
import yt_dlp
import tempfile

def display_tracker_options():
        tracker_type = "bytetrack.yaml"
        is_display_tracker = True
        return is_display_tracker, tracker_type

def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None):
    # Resize the image to a standard size
    scale_percent = 60 # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    # Display object tracking, if specified
    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker)
    else:
        # Predict the objects in the image using the YOLOv8 model
        res = model.predict(image, conf=conf)
    # # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )

def get_youtube_stream_url(youtube_url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'no_warnings': True,
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url']

def play_youtube_video(conf, model):
    st.title("Butterfly Detection on Video URL Input")
    source_youtube = st.text_input("Enter or paste your URL below: ")
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect'):
        if not source_youtube:
            st.sidebar.error("Please enter a YouTube URL")
            return
        try:
            st.sidebar.info("Extracting video stream URL...")
            stream_url = get_youtube_stream_url(source_youtube)
            st.sidebar.info("Opening video stream...")
            vid_cap = cv2.VideoCapture(stream_url)
            if not vid_cap.isOpened():
                st.sidebar.error(
                    "Failed to open video stream. Please try a different video.")
                return
            st.sidebar.success("Video stream opened successfully!")
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(
                        conf,
                        model,
                        st_frame,
                        image,
                        is_display_tracker,
                        tracker
                    )
                else:
                    break
            vid_cap.release()
        except Exception as e:
            st.sidebar.error(f"An error occurred: {str(e)}")

def play_stored_video(conf, model):
    st.title("Butterfly Detection on Video Input")
    file = st.file_uploader("Choose a video...",type=("mp4"))
    if file is not None:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name
    else:
        st.write("No video chosen")
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect'):
        try:
            vid_cap = cv2.VideoCapture(str(temp_file_path))
            st_frame = st.empty()
            while vid_cap.isOpened():
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))
