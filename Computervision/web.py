import cv2
import time
import json
import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import requests
from io import BytesIO

# Tải mô hình YOLO
model = YOLO("models/momo.pt")

# Khởi tạo ứng dụng Streamlit
st.title("Nhận diện Động vật với YOLOv8")
st.markdown("Chọn nguồn dữ liệu để nhận diện động vật: camera, tải ảnh lên, hoặc nhập URL ảnh.")

# Lựa chọn giữa camera, ảnh tải lên, và URL ảnh
source_option = st.radio("Chọn nguồn dữ liệu:", ("Camera", "Tải ảnh lên", "Nhập URL ảnh"))

# Khởi tạo danh sách lưu thông tin phát hiện
detection_info = []

# Khởi tạo từ điển đếm số lượng các lớp
class_count = {}

# Chức năng xử lý ảnh tải lên từ máy tính
if source_option == "Tải ảnh lên":
    uploaded_file = st.file_uploader("Chọn một hình ảnh để nhận diện", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Đọc ảnh từ file
        image = Image.open(uploaded_file)
        
        # Chuyển ảnh từ PIL sang OpenCV (BGR)
        frame = np.array(image)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Thực hiện suy luận với mô hình YOLO
        results = model(frame)

        # Kết quả trả về là một danh sách các đối tượng phát hiện (results[0] là cho ảnh đầu tiên)
        boxes = results[0].boxes.xyxy.cpu().numpy()  # Toạ độ bounding box (x1, y1, x2, y2)
        confidences = results[0].boxes.conf.cpu().numpy()  # Điểm tin cậy của các đối tượng
        class_ids = results[0].boxes.cls.cpu().numpy()  # ID lớp của các đối tượng
        
        current_time = time.time()  # Lấy thời gian hiện tại (tính theo giây từ epoch)

        # Vẽ các bounding box cho những đối tượng có điểm tin cậy > 80%
        for i, box in enumerate(boxes):
            confidence = confidences[i]
            
            # Bỏ qua những đối tượng có điểm tin cậy thấp hơn 85%
            if confidence < 0.85:
                continue
            
            # Lấy toạ độ của bounding box
            x1, y1, x2, y2 = box
            
            # Lấy nhãn lớp
            class_id = int(class_ids[i])
            label = results[0].names[class_id]
            
            # Vẽ hình chữ nhật xung quanh đối tượng phát hiện
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            
            # Hiển thị nhãn lớp trên bounding box
            text = f"{label}"
            cv2.putText(frame, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Lưu thông tin phát hiện vào danh sách
            detection_info.append({
                "class": label,
                "start_time": current_time,
                "end_time": None,  # Cập nhật khi đối tượng biến mất
            })
            
            # Cập nhật số lượng lớp đã phát hiện
            if label in class_count:
                class_count[label] += 1
            else:
                class_count[label] = 1

        # Chuyển đổi ảnh từ BGR sang RGB để hiển thị trong Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, channels="RGB", use_container_width=True)
        
        # Hiển thị số lượng các lớp phát hiện dưới ảnh
        st.write("Số lượng các lớp phát hiện:")
        st.write(class_count)

        # Lưu thông tin phát hiện vào file JSON
        with open('detection_info.json', 'w') as f:
            json.dump(detection_info, f, indent=4)

# Chức năng xử lý ảnh từ URL
if source_option == "Nhập URL ảnh":
    image_url = st.text_input("Nhập URL của hình ảnh để nhận diện")

    if image_url:
        try:
            # Tải ảnh từ URL
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            # Chuyển ảnh từ PIL sang OpenCV (BGR)
            frame = np.array(image)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Thực hiện suy luận với mô hình YOLO
            results = model(frame)

            # Kết quả trả về là một danh sách các đối tượng phát hiện (results[0] là cho ảnh đầu tiên)
            boxes = results[0].boxes.xyxy.cpu().numpy()  # Toạ độ bounding box (x1, y1, x2, y2)
            confidences = results[0].boxes.conf.cpu().numpy()  # Điểm tin cậy của các đối tượng
            class_ids = results[0].boxes.cls.cpu().numpy()  # ID lớp của các đối tượng
            
            current_time = time.time()  # Lấy thời gian hiện tại (tính theo giây từ epoch)

            # Vẽ các bounding box cho những đối tượng có điểm tin cậy > 80%
            for i, box in enumerate(boxes):
                confidence = confidences[i]
                
                # Bỏ qua những đối tượng có điểm tin cậy thấp hơn 85%
                if confidence < 0.85:
                    continue
                
                # Lấy toạ độ của bounding box
                x1, y1, x2, y2 = box
                
                # Lấy nhãn lớp
                class_id = int(class_ids[i])
                label = results[0].names[class_id]
                
                # Vẽ hình chữ nhật xung quanh đối tượng phát hiện
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                # Hiển thị nhãn lớp trên bounding box
                text = f"{label}"
                cv2.putText(frame, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Lưu thông tin phát hiện vào danh sách
                detection_info.append({
                    "class": label,
                    "start_time": current_time,
                    "end_time": None,  # Cập nhật khi đối tượng biến mất
                })
                
                # Cập nhật số lượng lớp đã phát hiện
                if label in class_count:
                    class_count[label] += 1
                else:
                    class_count[label] = 1

            # Chuyển đổi ảnh từ BGR sang RGB để hiển thị trong Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame_rgb, channels="RGB", use_container_width=True)
            
            # Hiển thị số lượng các lớp phát hiện dưới ảnh
            st.write("Số lượng các lớp phát hiện:")
            st.write(class_count)

            # Lưu thông tin phát hiện vào file JSON
            with open('detection_info.json', 'w') as f:
                json.dump(detection_info, f, indent=4)

        except Exception as e:
            st.error(f"Không thể tải ảnh từ URL. Lỗi: {e}")

# Chức năng xử lý video từ camera
if source_option == "Camera":
    cap = cv2.VideoCapture(0)  # Sử dụng camera mặc định
    
    if not cap.isOpened():
        st.error("Không thể mở camera.")
    else:
        # Tạo một placeholder cho video
        frame_placeholder = st.empty()

        # Khởi tạo từ điển đếm số lượng các lớp
        class_count_camera = {}

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Thực hiện suy luận với mô hình YOLO
            results = model(frame)

            # Kết quả trả về là một danh sách các đối tượng phát hiện (results[0] là cho ảnh đầu tiên)
            boxes = results[0].boxes.xyxy.cpu().numpy()  # Toạ độ bounding box (x1, y1, x2, y2)
            confidences = results[0].boxes.conf.cpu().numpy()  # Điểm tin cậy của các đối tượng
            class_ids = results[0].boxes.cls.cpu().numpy()  # ID lớp của các đối tượng
            
            current_time = time.time()  # Lấy thời gian hiện tại (tính theo giây từ epoch)

            # Vẽ các bounding box cho những đối tượng có điểm tin cậy > 80%
            for i, box in enumerate(boxes):
                confidence = confidences[i]
                
                # Bỏ qua những đối tượng có điểm tin cậy thấp hơn 85%
                if confidence < 0.85:
                    continue
                
                # Lấy toạ độ của bounding box
                x1, y1, x2, y2 = box
                
                # Lấy nhãn lớp
                class_id = int(class_ids[i])
                label = results[0].names[class_id]
                
                # Vẽ hình chữ nhật xung quanh đối tượng phát hiện
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                # Hiển thị nhãn lớp trên bounding box
                text = f"{label}"
                cv2.putText(frame, text, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Lưu thông tin phát hiện vào danh sách
                detection_info.append({
                    "class": label,
                    "start_time": current_time,
                    "end_time": None,  # Cập nhật khi đối tượng biến mất
                })
                
                # Cập nhật số lượng lớp đã phát hiện
                if label in class_count_camera:
                    class_count_camera[label] += 1
                else:
                    class_count_camera[label] = 1

            # Chuyển đổi ảnh từ BGR sang RGB để hiển thị trong Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(frame_rgb, channels="RGB", use_container_width=True)
            
            # Hiển thị số lượng các lớp phát hiện dưới video
            st.write("Số lượng các lớp phát hiện:")
            st.write(class_count_camera)

            # Thoát vòng lặp nếu người dùng nhấn phím 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Giải phóng tài nguyên khi kết thúc
        cap.release()
