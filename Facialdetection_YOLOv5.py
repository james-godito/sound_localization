import cv2
import torch

# Load YOLOv5 model (change the path to your trained model)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def main():
    # Initialize webcam (usually index 0 for the default camera)
    cap = cv2.VideoCapture(2)

    if not cap.isOpened():
        print("Error: Webcam not found or cannot be opened.")
        return

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Cannot read frame from webcam.")
            break

        # Perform inference using YOLOv5
        results = model(frame)

        # Get coordinates of detected people
        for det in results.pred[0]:
            if det[-1] == 0:  # Class index for "person"
                x, y, w, h = det[:4]
                center_x = int(x + w / 2)
                center_y = int(y + h / 2)
                print(f"Person at (x, y): ({center_x}, {center_y})")

        # Display the frame
        cv2.imshow("Webcam Feed", frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
