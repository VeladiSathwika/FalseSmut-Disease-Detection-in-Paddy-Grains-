This project presents a Convolutional Neural Network (CNN)-based model for detecting False Smut Disease in paddy grains.
It focuses on image classification techniques using supervised learning to differentiate healthy grains from infected ones with high accuracy and robustness.
The CNN model was evaluated using multiple performance metrics:
For Healthy grain detection:
- Accuracy: 92%
- Precision: 91%
- Recall: 97%
- F1-Score: 94% 
For infected grain detection:
- Precision (Infected): 94%
- Recall (Infected): 84%
- F1-Score (Infected): 89%
🧪 Dataset
Training and testing were conducted on a combination of publicly available paddy grain images and artificially generated false smut-infected samples. These were preprocessed to improve clarity and enhance model learning.
🧰 Technologies Used
- Python
- TensorFlow and Keras 
- OpenCV for image handling
- CNN architecture 
📦 Features
- Image classification into "Healthy" and "False Smut Infected"
- Aggregated evaluation at image level
- Visualization of training vs. validation accuracy
- Modular code design for easy extension
📌 How to Run
python -m streamlit run app.py
🛠️ Future Enhancements
- Integration of temporal data for tracking disease progression
- Inclusion of multimodal inputs like spectral imagery and metadata
- Real-time detection module with deployment on mobile or edge devices
