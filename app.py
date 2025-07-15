import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image

# TensorFlow Model Prediction
def model_prediction(test_image):
    try:
        # Load the trained model
        model = tf.keras.models.load_model('false_smut_model.keras')
        
        # Preprocess the uploaded image
        image = Image.open(test_image)  # Ensure compatibility with uploaded files
        image = image.resize((128, 128))  # Resize image to match model input size
        input_arr = np.array(image) / 255.0  # Normalize pixel values to [0,1]
        input_arr = np.expand_dims(input_arr, axis=0)  # Add batch dimension
        
        # Predict using the model
        prediction = model.predict(input_arr)[0][0]  # Binary prediction outputs a single probability
        
        # Confidence level
        confidence = round(prediction * 100, 2) if prediction >= 0.5 else round((1 - prediction) * 100, 2)
        
        # Ensure correct threshold logic for predictions
        result = "false_smut" if prediction >= 0.5 else "fs_absent"
        return result, confidence
    
    except Exception as e:
        return f"Error during prediction: {e}", None

# CSS for styling the page, sidebar, buttons, browse button, drag-and-drop box, and text inside it
custom_css = '''
<style>
.stApp {
    background-image: url("https://slidescorner.com/wp-content/uploads/2022/08/01-500x281.jpg");
    background-size: cover;
    background-color: white; /* Sets main background to white */
    color: black; /* Ensures main text color is black */
}

[data-testid="stSidebar"] {
    background-image: url("https://th.bing.com/th/id/OIP.RAMbUcWAe3QT31OwCuiBrAAAAA?pid=ImgDet&w=178&h=267&c=7&dpr=1.5");
    background-size: cover;
    background-color: white; /* Sets sidebar background to white */
    color: black; /* Ensures sidebar text is black */
    font-size: 18px; /* Optional: Adjust sidebar text size */
    border-right: 2px solid #ccc; /* Adds a subtle border to the right of the sidebar */
    box-shadow: 2px 0 5px rgba(0,0,0,0.1); /* Adds a shadow to make the sidebar stand out */
}

header .css-18ni7ap.e8zbici0 { 
    background-color: white; /* Changes the top bar (header) background to white */
    color: black; /* Ensures header text is black for visibility */
    border-bottom: 1px solid #ddd; /* Optional: Adds a subtle border below the header */
}

/* Button Styling */
button {
    background-color: white !important; /* Makes button background white */
    color: black !important; /* Makes button text black */
    border: 1px solid #ccc; /* Adds a subtle border to the button */
    font-size: 16px; /* Adjusts button font size */
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1); /* Adds a subtle shadow for better visuals */
    padding: 0.5em 1em; /* Optional: Adjusts padding for button size */
}

button:hover {
    background-color: #f2f2f2 !important; /* Slightly changes background on hover for better feedback */
}

/* Browse Button Styling */
input[type="file"]::file-selector-button {
    background-color: white; /* Makes Browse button background white */
    color: black; /* Makes Browse button text black */
    border: 1px solid #ccc; /* Adds a border to the Browse button */
    padding: 0.5em 1em; /* Adjusts padding for button size */
    font-size: 16px; /* Adjusts text font size */
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1); /* Adds a subtle shadow for better visuals */
    cursor: pointer; /* Ensures pointer cursor on hover */
}

input[type="file"]::file-selector-button:hover {
    background-color: #f2f2f2; /* Slightly changes background on hover */
}

/* Drag-and-Drop Box Styling */
div[data-testid="stFileUploader"] {
    background-color: white; /* Makes drag-and-drop box background white */
    border: 2px dashed #ccc; /* Adds a dashed border around the box */
    border-radius: 10px; /* Adds rounded corners */
    padding: 10px; /* Adjusts padding for better spacing */
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1); /* Adds a shadow for better visuals */
    color: black; /* Ensures text inside the drag-and-drop box is black */
}

div[data-testid="stFileUploader"] label {
    color: black !important; /* Changes "Choose an Image" text to black */
}

div[data-testid="stFileUploader"]:hover {
    background-color: #f2f2f2; /* Changes background slightly on hover */
}
</style>
'''

st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About", "Disease Recognition"])

# Home Page
if app_mode == "Home":
    st.header("FALSE SMUT DISEASE DETECTOR")
    image_path = "home_page.jpeg"  # Ensure this file exists in your working directory
    try:
        st.image(image_path, use_container_width=True)  # Updated parameter
    except Exception:
        st.write("Home page image not found.")
    st.markdown("""
    Welcome to the False Smut Detection System! 🌾🔍

    ### Get Started
    Click on the **Disease Recognition** page in the sidebar to upload an image and detect False Smut in paddy grains.
    """)

# About Page
elif app_mode == "About":
    st.header("About")
    st.markdown("""
    ### Dataset
    This project focuses on detecting False Smut in paddy grains. The dataset consists of images categorized into two classes:
    - **false_smut**: Images showing signs of the disease.
    - **fs_absent**: Images without any signs of the disease.
    """)
    st.markdown("""
    ### Accuracy
    The trained model achieved a classification accuracy of **95%** during testing on a validation dataset.
    """)

# Disease Recognition Page
elif app_mode == "Disease Recognition":
    st.header("Disease Recognition")
    test_image = st.file_uploader("Choose an Image:")
    
    # Show Image Button
    if st.button("Show Image"):
        if test_image is not None:
            try:
                st.image(test_image, use_column_width=True)  # Updated parameter
            except Exception as e:
                st.write(f"Error displaying image: {e}")
        else:
            st.write("Please upload an image to display.")
    
    # Predict Button
    if st.button("Predict"):
        if test_image is not None:
            with st.spinner("Please Wait..."):
                try:
                    result, confidence = model_prediction(test_image)
                    if confidence is not None:
                        st.markdown(f"<p style='color:black;'>Model predicts: <strong>{result}</strong></p>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color:black;'>Confidence Level: <strong>{confidence}%</strong></p>", unsafe_allow_html=True)
                    else:
                        st.error(result)
                except Exception as e:
                    st.error(f"Error during prediction: {e}")
        else:
            st.write("Please upload an image to predict.")
