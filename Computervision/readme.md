# Project introduction
## Title: Object-animal recognition system with YOLOv8 and Streamlit
This project is developed to build an animal recognition system using the YOLOv8 (You Only Look Once) model – one of the most advanced deep learning models for object detection in images and videos. The system will provide a user-friendly interface using Streamlit, allowing users to choose from multiple data sources, such as a camera, uploading images, or entering image URLs from the web, to perform animal recognition.
## How to run the system
Python 3.7 - 3.11

pip install -r requiments.txt or pip3 install -r requiments.txt

with win: python -m streamlit run web.py. With linux: python3 -m streamlit run web.py
##  Frontend 
![image](https://github.com/user-attachments/assets/4cd8c1f2-409f-4c8b-856c-02a175acbdf6)
Technology: Streamlit
Functions:
Display Images/Videos: The user interface allows the display of images or videos directly from the camera.
Upload Images: Users can upload images from their computer.
Enter Image URL: Users can input the URL of an image from websites, and the system will automatically fetch the image and perform recognition.
Display Results: After recognition, the results are displayed with bounding boxes drawn around the animal objects, along with class labels and the count of each class.
Display Statistics: The system summarizes and shows the count of recognized animal classes in each image or video.
User Interface:
The application's interface is simple and easy to use, enabling users to easily select data sources and view recognition results instantly.
## Backend (Processing and Logic):
Technology: YOLOv8 (Ultralytics), OpenCV, Requests
Functions:
Object Detection with YOLOv8: The system uses the YOLOv8 model to detect animal objects in images or videos. YOLOv8 is an advanced deep learning model known for its real-time object detection capability and high accuracy.
Live Video Processing: OpenCV is used to process live video from the camera and feed it directly into the detection system.
Image Processing from Upload and URL: The system uses the PIL library to load images from the computer and the Requests library to fetch images from URLs provided by users.
Store Detection Information: All information related to detected objects, including class labels, detection time, and bounding box coordinates, will be saved in a JSON file (detection_info.json) for users to review later.
## total 
![image](https://github.com/user-attachments/assets/48e60ae2-e83e-416c-a98c-0fc4ccc69d54)




