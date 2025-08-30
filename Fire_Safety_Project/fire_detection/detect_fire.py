import cv2
import json
import time

# Path to store fire status
STATUS_FILE = "fire_status.json"

def update_fire_status(status):
    """Write fire detection result to a JSON file"""
    with open(STATUS_FILE, "w") as f:
        json.dump({"fire_detected": status, "timestamp": time.time()}, f)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define fire-like color range (better tuned)
    lower = (0, 50, 50)     # red/orange start
    upper = (35, 255, 255)  # yellow end

    mask = cv2.inRange(hsv, lower, upper)

    fire_detected = cv2.countNonZero(mask) > 15000

    if fire_detected:
        cv2.putText(frame, "🔥 FIRE DETECTED!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        update_fire_status(1)
    else:
        update_fire_status(0)

    cv2.imshow("Fire Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
