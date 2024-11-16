from PIL import Image
from transformers import VisionEncoderDecoderModel, AutoTokenizer, AutoFeatureExtractor

# Load pre-trained model and tokenizer
model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = AutoFeatureExtractor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

def generate_caption(image_path):
    try:
        # Open and preprocess the image
        image = Image.open(image_path).convert("RGB")
        pixel_values = feature_extractor(images=image, return_tensors="pt").pixel_values

        # Generate captions
        output_ids = model.generate(pixel_values, max_length=16, num_beams=4)
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        raise ValueError(f"Error processing image: {e}")