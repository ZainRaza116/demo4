import cv2
import numpy as np
from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse

# Function to process each frame
def image_set(img):
    # Convert to grayscale and apply histogram equalization
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(gray)

    # Apply Gaussian blur to reduce noise and smoothen edges
    blurred = cv2.GaussianBlur(src=equ, ksize=(3, 5), sigmaX=0.5)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred, 70, 135)

    return edges

# Generator function to capture webcam frames and apply the filter
def webcam_feed():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        yield (b'--frame\r\nContent-Type: text/html\r\n\r\n', b'Error: Could not open webcam.\r\n')

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        processed_frame = image_set(frame)
        _, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()


def webcam_view(request):
    try:
        return StreamingHttpResponse(webcam_feed(), content_type='multipart/x-mixed-replace; boundary=frame')
    except:
        pass

def file_uploading(request):
    return render(request, 'fileuploading.html')
