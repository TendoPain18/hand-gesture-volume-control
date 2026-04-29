import cv2

# Open a video capture device (e.g., webcam)
cap = cv2.VideoCapture(0)  # Change the parameter to the appropriate video file if not using a webcam

# Check if the video capture device was opened successfully
if not cap.isOpened():
    print("Error: Could not open video capture device.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Get the dimensions of the frame
    height, width, _ = frame.shape

    # Define the region of interest (ROI) to zoom in
    # Example: Zoom in by cropping the center of the frame
    zoom_factor = 2  # Adjust this value to control the zoom level
    zoom_width = int(width / zoom_factor)
    zoom_height = int(height / zoom_factor)
    start_x = int((width - zoom_width) / 2)
    start_y = int((height - zoom_height) / 2)
    end_x = start_x + zoom_width
    end_y = start_y + zoom_height

    # Crop the frame to the ROI
    zoomed_frame = frame[start_y:end_y, start_x:end_x]

    # Resize the zoomed frame to the original frame size
    zoomed_frame = cv2.resize(zoomed_frame, (width, height))

    # Display the zoomed frame
    cv2.imshow('Zoomed Frame', zoomed_frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
