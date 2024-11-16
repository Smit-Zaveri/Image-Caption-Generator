import streamlit as st
import requests
from PIL import Image
import tempfile
import os

st.title("Image Caption Generator")

# Function to clear the temp image if it exists
def clear_temp_image(temp_image_path):
    if os.path.exists(temp_image_path):
        try:
            os.remove(temp_image_path)
        except PermissionError:
            st.error(f"Failed to remove the temporary file: {temp_image_path}. It might be in use by another process.")
        except Exception as e:
            st.error(f"Error removing temporary file: {e}")

# Upload image
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # Open the image to determine the format
    image = Image.open(uploaded_image)
    image_format = image.format.lower()  # Get the format of the image (png, jpeg, etc.)
    
    # Create a temporary image file path
    temp_image_path = f"./temp_image.{image_format}"
    
    # Clear the previous temporary image file if it exists
    clear_temp_image(temp_image_path)

    # Save the uploaded image as a temporary file
    with open(temp_image_path, "wb") as temp_file:
        temp_file.write(uploaded_image.getbuffer())  # Write the content of the uploaded image to the temp file

    # Display the uploaded image
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Handle caption generation
    if st.button("Generate Caption"):
        st.write("Generating caption, please wait...")
        with st.spinner("Processing..."):
            # Send image to backend
            with open(temp_image_path, "rb") as img_file:
                files = {"image": img_file}
                try:
                    response = requests.post("http://127.0.0.1:5000/generate_caption", files=files)

                    if response.status_code == 200:
                        st.success(f"Caption: {response.json()['caption']}")
                    else:
                        st.error(f"Failed to generate caption: {response.json().get('error', 'Unknown error')}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to backend: {e}")

    # Clear temporary file after processing
    clear_temp_image(temp_image_path)
