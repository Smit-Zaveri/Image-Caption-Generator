from flask import Flask, request, jsonify
from model import generate_caption
from PIL import Image, UnidentifiedImageError
import os
import tempfile

app = Flask(__name__)

@app.route("/generate_caption", methods=["POST"])
def caption_image():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    image = request.files["image"]
    image_filename = image.filename
    image_format = image_filename.split('.')[-1].lower()

    # Create a unique temp file for each request
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{image_format}") as temp_file:
        temp_file_path = temp_file.name
        image.save(temp_file_path)

    try:
        # Validate the image
        with Image.open(temp_file_path) as img:
            img = img.convert("RGB")  # Ensure a valid format for further processing
            app.logger.info(f"Image successfully validated: {image_filename}")

    except UnidentifiedImageError:
        app.logger.error(f"Uploaded file is not a valid image: {image_filename}")
        return jsonify({"error": "Uploaded file is not a valid image"}), 400
    except Exception as e:
        app.logger.error(f"Error processing image: {e}")
        return jsonify({"error": "Error processing image"}), 500

    try:
        # Generate caption
        caption = generate_caption(temp_file_path)
        return jsonify({"caption": caption})
    except Exception as e:
        app.logger.error(f"Error generating caption: {e}")
        return jsonify({"error": "Failed to generate caption"}), 500

    finally:
        # Clean up the temp file after processing
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
