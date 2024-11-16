import streamlit as st
import requests
from PIL import Image
import tempfile
import os

# App Configuration
st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🖼️",
    layout="wide",
)

# App Title and Description
st.markdown(
    """
    <div style="text-align: center; font-size: 2rem; color: #2D4A8A; font-weight: bold; margin-bottom: 1rem;">
        🖼️ AI Image Caption Generator
    </div>
    <div style="text-align: center; font-size: 1.2rem; color: #5A5A5A; margin-bottom: 2rem;">
        Upload an image and let our AI generate a descriptive caption for it.
    </div>
    <hr style="border-top: 1px solid #ddd;">
    """,
    unsafe_allow_html=True,
)

# Function to handle temporary file creation and cleanup
def handle_temp_image(uploaded_image):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    with temp_file as tf:
        tf.write(uploaded_image.getbuffer())
    return temp_file.name

# Main Container for Content
with st.container():
    # Two-Column Layout
    col1, col2 = st.columns([1, 2], gap="large")  # Adjust column proportions and spacing

    with col1:
        # Upload Image Section
        st.markdown(
            """
            <div style="font-size: 1.5rem; color: #2D4A8A; font-weight: bold; margin-bottom: 1rem;">
                📤 Upload Your Image
            </div>
            """,
            unsafe_allow_html=True,
        )
        uploaded_image = st.file_uploader(
            "Upload an image (JPEG, PNG)", type=["jpg", "jpeg", "png"]
        )

        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image Preview", use_container_width=True)

    with col2:
        # Generate Caption Section
        st.markdown(
            """
            <div style="font-size: 1.5rem; color: #2D4A8A; font-weight: bold; margin-bottom: 1rem;">
                🧠 Generate a Caption
            </div>
            """,
            unsafe_allow_html=True,
        )
        if uploaded_image:
            if st.button("✨ Generate Caption"):
                st.write("Analyzing the image... This may take a few seconds.")
                with st.spinner("🔄 AI is working on your image..."):
                    # Handle temporary image saving
                    temp_image_path = handle_temp_image(uploaded_image)

                    try:
                        # Send image to backend
                        with open(temp_image_path, "rb") as img_file:
                            response = requests.post(
                                "http://127.0.0.1:5000/generate_caption", files={"image": img_file}
                            )

                        # Handle Backend Response
                        if response.status_code == 200:
                            caption = response.json().get("caption", "No caption received.")
                            st.success(f"**Generated Caption:** {caption}")
                        else:
                            error_message = response.json().get("error", "Unknown error occurred.")
                            st.error(f"❌ Failed to generate caption: {error_message}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"⚠️ Error connecting to the backend: {e}")
                    finally:
                        # Cleanup temporary file
                        if os.path.exists(temp_image_path):
                            os.remove(temp_image_path)

# Footer Section
st.markdown("<hr style='border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; font-size: 1rem; color: #5A5A5A; margin-top: 1rem;">
        Made with ❤️ by <a href="https://github.com/Smit-Zaveri" target="_blank" style="color: #2D4A8A; text-decoration: none;">Smit Zaveri</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Custom CSS for Modern UI
st.markdown(
    """
    <style>
    /* Main Container */
    .stApp {
        padding: 1rem; /* Add space around the app */
    }

    /* Columns */
    .css-1cpxqw2 {  /* Adjust column padding */
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2D4A8A;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #1B3375;
    }

    /* Uploaded Image */
    .stImage {
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Spinner */
    .stSpinner {
        font-size: 1.2rem;
        color: #2D4A8A;
    }

    /* Footer */
    footer {
        text-align: center;
        font-size: 0.9rem;
    }
    footer a {
        color: #2D4A8A;
        text-decoration: none;
    }
    footer a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
