import cv2
import torch
from yolov5 import YOLOv5

image_path = ''

# Define the output path for the processed image
output_image_path = ''


model = YOLOv5('yolov5s', device='cpu')

image = cv2.imread(image_path)


results = model(image)


vehicle_classes = ['car', 'motorcycle', 'bus', 'truck']  # Define the classes you consider as vehicles
vehicle_count = 0


for detection in results.xyxy[0]:  # Iterate over the detections in the image
    class_id = int(detection[5])  # Class ID of the detection
    confidence = float(detection[4])  # Confidence score of the detection
    if confidence > 0.5:  # Filter detections based on confidence threshold (e.g., > 0.5)
        # Get the class name from the model's class names
        class_name = model.names[class_id]
        
        # Check if the class name is a vehicle class
        if class_name in vehicle_classes:
            vehicle_count += 1
            
            # Draw a bounding box and label on the image
            x1, y1, x2, y2 = map(int, detection[:4])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{class_name} ({confidence:.2f})"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

cv2.imwrite(output_image_path, image)

print(f"Number of vehicles detected: {vehicle_count}")
print(f"Processed image with bounding boxes saved to {output_image_path}")