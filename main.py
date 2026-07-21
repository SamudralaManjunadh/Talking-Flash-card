import cv2
import json
import pygame
import os

print("Program Started")

# -----------------------------
# Load Flash Card Dictionary
# -----------------------------
with open("cards.json", "r") as file:
    cards = json.load(file)

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()
pygame.mixer.init()

# -----------------------------
# QR Detector
# -----------------------------
detector = cv2.QRCodeDetector()

# -----------------------------
# Webcam
# -----------------------------
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Could not open webcam!")
    exit()

# -----------------------------
# Variables
# -----------------------------
last_detected = ""

print("===================================")
print(" Talking Flash Card Reader Started ")
print(" Show a QR Card")
print(" Press Q to Exit")
print("===================================")

while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera Error!")
        break

    # -----------------------------
    # Detect QR Code
    # -----------------------------
    data, bbox, _ = detector.detectAndDecode(frame)

    # -----------------------------
    # Draw QR Box
    # -----------------------------
    if bbox is not None:

        bbox = bbox.astype(int)

        for i in range(len(bbox[0])):
            pt1 = tuple(bbox[0][i])
            pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])

            cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

    # -----------------------------
    # QR Detected
    # -----------------------------
    if data:

        code = data.strip().upper()

        if code in cards:

            word = cards[code]

            cv2.putText(
                frame,
                word,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )

            # Speak only when NEW card appears
            if code != last_detected:

                print("--------------------------------")
                print("Detected :", code)
                print("Word     :", word)

                audio_file = f"audio/{code}.mp3"

                if os.path.exists(audio_file):

                    try:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(audio_file)
                        pygame.mixer.music.play()

                        print("Playing:", audio_file)

                    except Exception as e:
                        print("Audio Error:", e)

                else:
                    print("Audio File Missing:", audio_file)

                last_detected = code

        else:

            cv2.putText(
                frame,
                "Unknown Card",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

    else:
        # Reset when QR disappears
        last_detected = ""

    # -----------------------------
    # Show Camera
    # -----------------------------
    cv2.imshow("Talking Flash Card Reader", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
pygame.quit()
