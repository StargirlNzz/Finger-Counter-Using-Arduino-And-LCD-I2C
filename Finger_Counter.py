import cv2
import mediapipe as mp
import serial
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize serial communication with Arduino
arduino_port = 'COM71'  # Change 'COM23' to your Arduino port
arduino = serial.Serial(arduino_port, 9600)  # Set baud rate to match Arduino
time.sleep(2)  # Wait for the connection to establish

# Function to count fingers
def count_fingers(lmlist):
    fingers = 0
    # Thumb
    if lmlist[4][1] < lmlist[3][1]:
        fingers += 1
    # Index
    if lmlist[8][2] < lmlist[7][2]:
        fingers += 1
    # Middle
    if lmlist[12][2] < lmlist[11][2]:
        fingers += 1
    # Ring
    if lmlist[16][2] < lmlist[15][2]:
        fingers += 1
    # Pinky
    if lmlist[20][2] < lmlist[19][2]:
        fingers += 1
    return fingers

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    fingers = 0
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

        lmlist = []
        for id, lm in enumerate(hand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmlist.append([id, cx, cy])

        if lmlist:
            fingers = count_fingers(lmlist)

        cv2.putText(img, f'{fingers}', (100, 300), cv2.FONT_HERSHEY_COMPLEX, 5, (0, 255, 0), 3)

        # Send the finger count to Arduino
        arduino.write(f'{fingers}\n'.encode())

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()