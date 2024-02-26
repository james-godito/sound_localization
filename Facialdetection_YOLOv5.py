import cv2
import torch
import serial
import time
import numpy as np

x_min = 800
x_max = 1120

# Provided camera matrix and distortion coefficients
cameraMatrix = np.array([[1124, 0, 929.81],
                         [0, 1122.3, 539.46],
                         [0, 0, 1]])
distCoeffs = np.array([[-0.41517, 0.22091, -0.00098211, -4.9035e-05, -0.063787]])

# Load YOLOv5 model (change the path to your trained model)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Initialize serial communication with Arduino (change to your Arduino's COM port)
ser = serial.Serial(port='COM3', baudrate=9600)

last_send_time = time.time()

def undistort_frame(frame):
    undistorted_frame = cv2.undistort(frame, cameraMatrix, distCoeffs)
    return undistorted_frame

def main():
    # Initialize webcam (usually index 0 for the default camera)
    cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print("Error: Webcam not found or cannot be opened.")
        return

    global last_send_time

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Cannot read frame from webcam.")
            break

        # Undistort the frame
        undistorted_frame = undistort_frame(frame)

        # Perform inference using YOLOv5
        results = model(undistorted_frame)

        # Get coordinates of detected people
        for det in results.pred[0]:
            if det[-1] == 0:  # Class index for "person"
                x, y, w, h = det[:4]
                center_x = int(x + w / 2)
                center_y = int(y + h / 2)

                current_time = time.time()
                if center_x < x_min or center_x > x_max and current_time - last_send_time >= 1:
                    ser.write(f"{center_x},{center_y}\n".encode())
                    last_send_time = current_time

        # Display the undistorted frame
        cv2.imshow("Undistorted Webcam Feed", undistorted_frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()
    ser.close()  # Close serial connection

if __name__ == "__main__":
    main()
