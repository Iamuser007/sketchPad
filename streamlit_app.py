import streamlit as st
from streamlit_drawable_canvas import st_canvas
from io import BytesIO
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64
import streamlit.components.v1 as components

# Title
st.title("Interactive Sketchpad")

# Sidebar settings
st.sidebar.title("Settings")
background_color = st.sidebar.selectbox(
    "Select background color", ["White", "Light Grey", "Custom"]
)

if background_color == "Light Grey":
    bg_color = "#d3d3d3"
elif background_color == "Custom":
    bg_color = st.sidebar.color_picker("Pick a color", "#ffffff")
else:
    bg_color = "#ffffff"

# Text options
text_input = st.sidebar.text_area("Add text to your sketch:")
text_color = st.sidebar.color_picker("Pick a text color", "#000000")
font_size = st.sidebar.slider("Select font size", 10, 50, 20)
add_text_button = st.sidebar.button("Add Text to Sketch")

# Canvas
canvas_result = st_canvas(
    stroke_color="black",
    stroke_width=2,
    background_color=bg_color,
    width=600,
    height=400,
    drawing_mode="freedraw",
    key="canvas",
)

# Helper to create download link
def trigger_download(file_data, file_name):
    download_link = f'''
        <a href="data:image/png;base64,{file_data}" 
           download="{file_name}" 
           style="display:none;" 
           id="autoDownload"></a>
        <script>
            document.getElementById("autoDownload").click();
        </script>
    '''
    components.html(download_link, height=0)

# If canvas has content
if canvas_result.image_data is not None:
    raw_image = Image.fromarray(canvas_result.image_data.astype(np.uint8))

    # Save raw image to bytes
    raw_buffer = BytesIO()
    raw_image.save(raw_buffer, format="PNG")
    raw_img_data = raw_buffer.getvalue()
    raw_base64 = base64.b64encode(raw_img_data).decode("utf-8")

    # Streamlit download button
    st.sidebar.download_button(
        label="Download Sketch",
        data=raw_img_data,
        file_name="sketch.png",
        mime="image/png"
    )

    # Auto-trigger download in WebView
    trigger_download(raw_base64, "sketch.png")

    # If user clicked to add text
    if add_text_button and text_input:
        text_image = raw_image.copy()
        draw = ImageDraw.Draw(text_image)
        font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text_input, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((text_image.width - text_width) // 2, text_image.height - text_height - 10)

        draw.text(position, text_input, fill=text_color, font=font)

        # Save text image
        text_buffer = BytesIO()
        text_image.save(text_buffer, format="PNG")
        text_img_data = text_buffer.getvalue()
        text_base64 = base64.b64encode(text_img_data).decode("utf-8")

        # Download button with text
        st.sidebar.download_button(
            label="Download Sketch with Text",
            data=text_img_data,
            file_name="sketch_with_text.png",
            mime="image/png"
        )

        # Trigger download with text
        trigger_download(text_base64, "sketch_with_text.png")

# Footer
st.markdown("""
<br><br>
🌟✨ **2025 April** ✨🌟  
Developed by **Mcpraise Leightong Okoi** with a nice handwriting and with love ❤️  
""", unsafe_allow_html=True)
