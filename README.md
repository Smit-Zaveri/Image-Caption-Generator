# Image Caption Generator

This project generates captions for uploaded images using a pre-trained deep learning model. The application consists of a Flask backend for image processing and a Streamlit frontend for user interaction.

## Features
- Upload images and receive a descriptive caption.
- Interactive progress indicator for caption generation.
- Lightweight, easy-to-deploy architecture.


## File Structure

```
image-caption-generator/ 
├── backend/ # Backend server and logic 
├── frontend/ # Frontend application 
├── README.md # Documentation 
└── .gitignore # Ignored files
```


## How to Run

### Prerequisites
- Python 3.8+
- Pip (Python package manager)

### Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/Smit-Zaveri/Image-Caption-Generator.git
   cd image-caption-generator
    ```

2. **Backend Setup**
   ```
   cd backend
   pip install -r requirements.txt
   python app.py
   ```
3. **Frontend Setup Open a new terminal and navigate to the frontend directory:**
   ```
   cd frontend
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. **Access the Application**

- Open http://localhost:8501 in your browser for the frontend.
- The backend runs at http://localhost:5000.

5. **Future Improvements**
- Add support for multiple caption suggestions.
- Enhance model with custom datasets.
- Deploy to cloud platforms like AWS or Heroku.

## **Credits**
- Pre-trained model: VisionEncoderDecoderModel


