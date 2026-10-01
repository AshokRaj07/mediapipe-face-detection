import mediapipe as mp
import cv2

# Define necessary options for face detection
BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Path to the face detection model
model_path = r"C:\Users\STUDENTS\Desktop\ASG\blaze_face_short_range.task"  # Update this path if needed

# Initialize MediaPipe FaceDetector
options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE
)

# Open webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

with FaceDetector.create_from_options(options) as detector:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Convert image to RGB (MediaPipe expects RGB format)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Run face detection
        detection_result = detector.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image))

        # Draw bounding boxes around detected faces
        for face in detection_result.detections:
            bboxC = face.bounding_box
            x, y = bboxC.origin_x, bboxC.origin_y
            w, h = bboxC.width, bboxC.height
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the output
        cv2.imshow('Face Detection', frame)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
