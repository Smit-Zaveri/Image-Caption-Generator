from flask import Flask, request, jsonify
from model import generate_caption
from PIL import Image, UnidentifiedImageError
import os
import tempfile
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = app.logger

def save_temp_image(uploaded_file):
    """Save the uploaded file to a temporary location."""
    file_extension = uploaded_file.filename.split('.')[-1].lower()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}")
    uploaded_file.save(temp_file.name)
    return temp_file.name

def validate_image(image_path):
    """Validate and preprocess the uploaded image."""
    try:
        with Image.open(image_path) as img:
            img.convert("RGB")  # Ensure the image is in RGB format
        return True
    except UnidentifiedImageError:
        logger.error(f"Invalid image format: {image_path}")
        return False
    except Exception as e:
        logger.error(f"Error validating image: {e}")
        return False

def cleanup_temp_file(file_path):
    """Remove the temporary file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Temporary file removed: {file_path}")
    except Exception as e:
        logger.warning(f"Failed to remove temporary file: {e}")

@app.route("/generate_caption", methods=["POST"])
def caption_image():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    uploaded_file = request.files["image"]

    # Save the uploaded image as a temporary file
    temp_file_path = save_temp_image(uploaded_file)
    logger.info(f"Uploaded image saved: {temp_file_path}")

    try:
        # Validate the image
        if not validate_image(temp_file_path):
            return jsonify({"error": "Uploaded file is not a valid image"}), 400

        # Generate the caption
        caption = generate_caption(temp_file_path)
        logger.info("Caption successfully generated")
        return jsonify({"caption": caption})

    except Exception as e:
        logger.error(f"Error during processing: {e}")
        return jsonify({"error": "An error occurred during caption generation"}), 500

    finally:
        # Clean up the temporary file
        cleanup_temp_file(temp_file_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
