import cv2
import serial
import numpy as np
import torch

def set_res(cap, x, y):
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))

ser = serial.Serial('COM3', 250000)  # Change if serial not COM3

cap = cv2.VideoCapture(0)

frame_w = 1920
frame_h = 1080
set_res(cap, frame_w, frame_h)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Our operations on the frame come here
    # Perform inference using YOLOv5
    results = model(frame)

    # Get coordinates of detected people
    detections = results.xyxy[0].cpu().numpy()

    # Filter detections to include only people (class 0)
    people_detections = detections[detections[:, -1] == 0]

    # Draw bounding boxes for people
    for det in people_detections:
        x, y, w, h, conf, cls = det
        x, y, w, h = int(x), int(y), int(w), int(h)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if people_detections.shape[0] > 0:
        # Assuming the first detected person is the closest one
        face_center_x = people_detections[0, 0] + people_detections[0, 2] / 2
        face_center_y = people_detections[0, 1] + people_detections[0, 3] / 2

        err_x = 30 * (face_center_x - frame_w / 2) / (frame_w / 2)
        err_y = 30 * (face_center_y - frame_h / 2) / (frame_h / 2)

        ser.write((f"{err_x}x!").encode())
        ser.write((f"{err_y}y!").encode())
        print("X:", err_x, "Y:", err_y)
    else:
        ser.write("o!".encode())

# When everything done, release the capture
ser.close()
cap.release()
cv2.destroyAllWindows()
