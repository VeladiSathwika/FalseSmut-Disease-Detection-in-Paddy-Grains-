import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# Load the trained TensorFlow model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('false_smut_model.keras')

model = load_model()

# Function to preprocess the image and predict
def model_prediction(image):
    try:
        # Preprocess the image
        image = image.resize((128, 128))  # Resize to match model input size
        input_arr = np.array(image) / 255.0  # Normalize pixel values to [0,1]
        input_arr = np.expand_dims(input_arr, axis=0)  # Add batch dimension
        
        # Predict using the model
        prediction = model.predict(input_arr)[0][0]  # Binary prediction outputs a single probability
        
        # Confidence level
        confidence = round(prediction * 100, 2) if prediction >= 0.5 else round((1 - prediction) * 100, 2)
        
        # Determine result
        result = "False Smut Detected" if prediction >= 0.5 else "No False Smut"
        return result, confidence
    except Exception as e:
        return f"Error during prediction: {e}", None
custom_css = '''
<style>
.stApp {
    background-image: url("https://slidescorner.com/wp-content/uploads/2022/08/01-500x281.jpg");
    background-size: cover;
    background-color: white; /* Sets main background to white */
    color: black; /* Ensures main text color is black */
}
</style>
'''
# Sidebar menu
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Recognition"])

# Home Page
if app_mode == "Home":
    st.header("FALSE SMUT DISEASE DETECTOR")
    image_path = "home_page.jpeg"  # Ensure this file exists in your working directory
    try:
        st.image(image_path, use_column_width=True)
    except Exception:
        st.write("Home page image not found.")
    st.markdown("""
    Welcome to the False Smut Detection System! 🌾🔍

    ### Get Started
    Click on the **Disease Recognition** page in the sidebar to upload an image or use your webcam to detect False Smut in paddy grains.
    """)

# About Page
elif app_mode == "About":
    st.header("About")
    st.markdown("""
    ### Dataset
    This project focuses on detecting False Smut in paddy grains. The dataset consists of images categorized into two classes:
    - **False Smut Detected**: Images showing signs of the disease.
    - **No False Smut**: Images without any signs of the disease.
    """)
    st.markdown("""
    ### Accuracy
    The trained model achieved a classification accuracy of **95%** during testing on a validation dataset. This may vary depending on the quality of the input image.
    """)

# Disease Recognition Page
elif app_mode == "Disease Recognition":
    st.header("Disease Recognition")

    # Webcam input
    st.subheader("Capture Image from Webcam")
    webcam_image = st.camera_input("Take a picture")

    if webcam_image is not None:
        # Convert webcam image to PIL format
        with st.spinner("Processing..."):
            img = Image.open(webcam_image)
            result, confidence = model_prediction(img)
            if confidence is not None:
                st.success(f"Model predicts: {result}")
                st.info(f"Confidence Level: {confidence}%")
            else:
                st.error(result)

    st.subheader("Upload Image for Detection")
    uploaded_image = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        with st.spinner("Processing..."):
            img = Image.open(uploaded_image)
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            result, confidence = model_prediction(img)
            if confidence is not None:
                st.success(f"Model predicts: {result}")
                st.info(f"Confidence Level: {confidence}%")
            else:
                st.error(result)
