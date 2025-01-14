import cv2
import numpy as np
import pyautogui
import math

# Function to calculate distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Initialize OpenCV camera
cap = cv2.VideoCapture(0)

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Blur the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply threshold to get binary image
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the largest contour (hand)
    if len(contours) > 0:
        hand_contour = max(contours, key=cv2.contourArea)
        
        # Get bounding box of the hand
        x, y, w, h = cv2.boundingRect(hand_contour)
        
        # Calculate centroid of the hand
        cx, cy = x + w // 2, y + h // 2
        
        # Draw a circle at the centroid
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
        
        # Map hand position to mouse movement
        screen_width, screen_height = pyautogui.size()
        mouse_x = int(np.interp(cx, [0, frame.shape[1]], [0, screen_width]))
        mouse_y = int(np.interp(cy, [0, frame.shape[0]], [0, screen_height]))
        pyautogui.moveTo(mouse_x, mouse_y)
        
        # Calculate hand gesture for volume control (example)
        if w > 100:
            volume = int(np.interp(h, [0, frame.shape[0]], [0, 100]))
            pyautogui.press('volumeup', presses=volume, interval=0.1)
        
    # Display the frame
    cv2.imshow('Frame', frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
