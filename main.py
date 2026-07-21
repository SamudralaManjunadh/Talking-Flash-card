import cv2
import pyttsx3
import json
import time
print("Program Started")
# -----------------------------
# Load Flash Card Dictionary
# -----------------------------
with open("cards.json", "r") as file:
    cards = json.load(file)

# -----------------------------
# Initialize Voice Engine
# -----------------------------
engine = pyttsx3.init()

engine.setProperty('rate', 140)
engine.setProperty('volume', 1)

# -----------------------------
# QR Detector
# -----------------------------
detector = cv2.QRCodeDetector()

# -----------------------------
# Webcam
# -----------------------------
camera = cv2.VideoCapture(0)

# -----------------------------
# Variables
# -----------------------------
last_card = ""
last_time = 0

print("===================================")
print(" Talking Flash Card Reader Started ")
print(" Press Q to Exit")
print("===================================")

while True:

    ret, frame = camera.read()

    if not ret:
        break

    data, bbox, _ = detector.detectAndDecode(frame)

    if bbox is not None:

        bbox = bbox.astype(int)

        n = len(bbox[0])

        for i in range(n):
            pt1 = tuple(bbox[0][i])
            pt2 = tuple(bbox[0][(i + 1) % n])
            cv2.line(frame, pt1, pt2, (0,255,0), 3)

    if data:

        code = data.strip().upper()

        if code in cards:

            word = cards[code]

            cv2.putText(
                frame,
                word,
                (30,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,0),
                2
            )

            current = time.time()

            if code != last_card or current-last_time > 3:

                print("Detected:", word)

                engine.say(word)
                engine.runAndWait()

                last_card = code
                last_time = current

        else:

            cv2.putText(
                frame,
                "Unknown Card",
                (30,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                2
            )

    cv2.imshow("Talking Flash Card Reader", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()