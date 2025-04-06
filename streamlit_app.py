import streamlit as st
from streamlit_drawable_canvas import st_canvas
from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pyttsx3
import sounddevice as sd
import wave
import tempfile

# Set title
st.title("Interactive Sketchpad with Voice Recording")

# Function to record audio from the device's microphone
def record_audio(duration=5, fs=44100):
    st.write("Recording... Speak now.")
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    return audio_data

# Function to save audio data to a file
def save_audio(audio_data):
    # Create a temporary file to save the audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_file, 'wb') as wf:
        wf.setnchannels(2)  # Stereo
        wf.setsampwidth(2)  # 2 bytes per sample
        wf.setframerate(44100)
        wf.writeframes(audio_data)
    return temp_file.name

# Sidebar for configuration
st.sidebar.title("Settings")
background_color = st.sidebar.selectbox(
    "Select background color", ["White", "Light Grey", "Custom"]
)

# Set the background color based on user's choice
if background_color == "Light Grey":
    bg_color = "#d3d3d3"
elif background_color == "Custom":
    bg_color = st.sidebar.color_picker("Pick a color", "#ffffff")
else:
    bg_color = "#ffffff"

# Text input for adding text to the canvas
text_input = st.sidebar.text_area("Add text to your sketch:")
text_color = st.sidebar.color_picker("Pick a text color", "#000000")
font_size = st.sidebar.slider("Select font size", 10, 50, 20)
add_text_button = st.sidebar.button("Add Text to Sketch")

# Create a drawing canvas where users can draw
canvas_result = st_canvas(
    stroke_color="black",
    stroke_width=2,
    background_color=bg_color,
    width=600,
    height=400,
    drawing_mode="freedraw",
    key="canvas",
)

# Initialize session state for audio recording
if 'recording' not in st.session_state:
    st.session_state.recording = False

if st.sidebar.button("Start Recording") and not st.session_state.recording:
    st.session_state.recording = True
    st.session_state.audio_data = sd.rec(int(1000000), samplerate=44100, channels=2, dtype='int16')
    st.write("Recording... Speak now.")

if st.sidebar.button("Stop Recording") and st.session_state.recording:
    st.session_state.recording = False
    sd.stop()  # Stop the recording
    st.write("Recording stopped.")
    
    # Save the audio to a file
    audio_file = save_audio(st.session_state.audio_data)
    
    # Provide download button for the audio file
    with open(audio_file, "rb") as f:
        st.sidebar.download_button(
            label="Download Audio Note",
            data=f,
            file_name="audio_note.wav",
            mime="audio/wav"
        )

# Button to add text to canvas
if add_text_button and text_input:
    # Display the text on the canvas as an image overlay
    canvas_image = Image.fromarray(canvas_result.image_data.astype(np.uint8))

    # Initialize ImageDraw
    draw = ImageDraw.Draw(canvas_image)

    # Add the text under the sketch
    font = ImageFont.load_default()

    # Calculate the text size using textbbox (Bounding Box)
    bbox = draw.textbbox((0, 0), text_input, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_position = ((canvas_image.width - text_width) // 2, canvas_image.height - text_height - 10)
    draw.text(text_position, text_input, fill=text_color, font=font)

    # Convert the image to a buffer for downloading
    buffered = BytesIO()
    canvas_image.save(buffered, format="PNG")
    img_data = buffered.getvalue()

    # Provide download button for the sketch with text
    st.sidebar.download_button(
        label="Download Sketch with Text",
        data=img_data,
        file_name="sketch_with_text.png",
        mime="image/png"
    )

# Option to download the raw sketch without text
if canvas_result.image_data is not None:
    pil_image = Image.fromarray(canvas_result.image_data.astype(np.uint8))

    # Save the image to a BytesIO buffer
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    img_data = buffered.getvalue()

    # Provide a download button for the raw sketch
    st.sidebar.download_button(
        label="Download Sketch",
        data=img_data,
        file_name="sketch.png",
        mime="image/png"
    )
    
st.markdown("""
<br><br>
🌟✨ **2025 April** ✨🌟  
Developed by **Mcpraise Leightong Okoi** with a nice handwriting and with love ❤️  
""", unsafe_allow_html=True)
