import streamlit as st
import qrcode
from PIL import Image
# import pywhatkit as kit
from io import BytesIO

# Function to generate QR code based on input type
def generate_qr_code(qr_type, data):
    if qr_type == "URL":
        qr = qrcode.make(data)
    elif qr_type == "Text":
        qr = qrcode.make(data)
    elif qr_type == "Email":
        qr = qrcode.make(f"mailto:{data}")
    elif qr_type == "Wi-Fi":
        qr = qrcode.make(f"WIFI:T:WPA;S:{data[0]};P:{data[1]};;")
    elif qr_type == "Contact Info":
        qr = qrcode.make(f"BEGIN:VCARD\nVERSION:3.0\nFN:{data[0]}\nTEL:{data[1]}\nEMAIL:{data[2]}\nEND:VCARD")
    elif qr_type == "SMS":
        qr = qrcode.make(f"SMS:{data[0]}?body={data[1]}")
    elif qr_type == "Location":
        qr = qrcode.make(f"geo:{data[0]},{data[1]}")
    elif qr_type == "Calendar Event":
        qr = qrcode.make(f"BEGIN:VEVENT\nSUMMARY:{data[0]}\nDTSTART:{data[1]}\nDTEND:{data[2]}\nLOCATION:{data[3]}\nEND:VEVENT")
    return qr

# Streamlit UI
st.title("QR Code Generator")

# Select the type of QR code
qr_type = st.selectbox("Choose the type of QR Code to generate", 
                       ["URL", "Text", "Email", "Wi-Fi", "Contact Info", "SMS", "Location", "Calendar Event"])

# Initialize qr_img to None
qr_img = None

# Input fields for the selected QR code type
if qr_type == "URL":
    url = st.text_input("Enter the URL")

elif qr_type == "Text":
    text = st.text_area("Enter the text")

elif qr_type == "Email":
    email = st.text_input("Enter the email address")

elif qr_type == "Wi-Fi":
    ssid = st.text_input("Enter the Wi-Fi SSID (Network name)")
    password = st.text_input("Enter the Wi-Fi password")

elif qr_type == "Contact Info":
    name = st.text_input("Enter the contact name")
    phone = st.text_input("Enter the phone number")
    email = st.text_input("Enter the email address")

elif qr_type == "SMS":
    phone_number = st.text_input("Enter the phone number")
    message = st.text_area("Enter the message")

elif qr_type == "Location":
    latitude = st.text_input("Enter latitude")
    longitude = st.text_input("Enter longitude")

elif qr_type == "Calendar Event":
    event_name = st.text_input("Enter the event name")
    start_time = st.text_input("Enter the start time (YYYYMMDDTHHMMSS)")
    end_time = st.text_input("Enter the end time (YYYYMMDDTHHMMSS)")
    location = st.text_input("Enter the event location")

# Confirm button to generate the QR code
if st.button("Generate QR Code"):
    if qr_type == "URL" and url:
        qr_img = generate_qr_code(qr_type, url)
    elif qr_type == "Text" and text:
        qr_img = generate_qr_code(qr_type, text)
    elif qr_type == "Email" and email:
        qr_img = generate_qr_code(qr_type, email)
    elif qr_type == "Wi-Fi" and ssid and password:
        qr_img = generate_qr_code(qr_type, [ssid, password])
    elif qr_type == "Contact Info" and name and phone and email:
        qr_img = generate_qr_code(qr_type, [name, phone, email])
    elif qr_type == "SMS" and phone_number and message:
        qr_img = generate_qr_code(qr_type, [phone_number, message])
    elif qr_type == "Location" and latitude and longitude:
        qr_img = generate_qr_code(qr_type, [latitude, longitude])
    elif qr_type == "Calendar Event" and event_name and start_time and end_time and location:
        qr_img = generate_qr_code(qr_type, [event_name, start_time, end_time, location])

    # If a QR code is generated, display it
    if qr_img:
        # Convert the QR code image to bytes
        img_bytes = BytesIO()
        qr_img.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        st.image(img_bytes)  # Display the QR code image

        # Save the QR code image and allow for download
        with open("qr_code.png", "wb") as f:
            f.write(img_bytes.getbuffer())
        
        st.download_button(
            label="Download QR Code",
            data=img_bytes,
            file_name="qr_code.png",
            mime="image/png"
        )

    
st.markdown("""
<br><br>
🌟✨ **2025 April** ✨🌟  
Developed by **Mcpraise Leightong Okoi** with a nice handwriting and with love ❤️  
""", unsafe_allow_html=True)
