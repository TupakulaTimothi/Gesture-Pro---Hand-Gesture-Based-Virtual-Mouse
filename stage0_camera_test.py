import cv2

# Start webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not found")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    cv2.imshow("Stage 0 - Camera Test", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()