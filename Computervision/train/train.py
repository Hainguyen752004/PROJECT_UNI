from ultralytics import YOLO

def train_model():
    model = YOLO("yolov8n.pt")  
    model.train(data="data.yaml", epochs=100, imgsz=640, device=0)
  
if __name__ == '__main__':
    train_model()  
