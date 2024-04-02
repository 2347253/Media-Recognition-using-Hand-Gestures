import cv2
import numpy as np
import av
import mediapipe as mp
from math import hypot
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import comtypes
import threading
    
comtypes.CoInitialize()

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# Get audio devices and initialize volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, -1, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Get volume range
volMin, volMax = volume.GetVolumeRange()[:2]

# Flag to keep track of play/pause state
is_playing = False

# Path to the video file
video_path = "cartoon.mp4"

# Initialize video capture object
cap = cv2.VideoCapture(video_path)

def process(image):
    global is_playing
    
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Initialize variables to store left and right hand landmarks
    left_hand_landmarks = None
    right_hand_landmarks = None
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            
            # Extract landmarks
            lmList = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            # Check if hand is on the right side of the frame
            if lmList and lmList[0][1] > w // 2:
                right_hand_landmarks = lmList
            elif lmList:
                left_hand_landmarks = lmList

    # Control volume based on left hand position
    if left_hand_landmarks:
        # Extract coordinates of key points (fingers)
        x1, y1 = left_hand_landmarks[4][1:3]  # Thumb tip
        x2, y2 = left_hand_landmarks[8][1:3]  # Index finger tip
                
        # Calculate distance between fingers
        length = hypot(x2 - x1, y2 - y1)

        # Interpolate distance to control volume
        vol = np.interp(length, [15, 220], [volMin, volMax])
        volume.SetMasterVolumeLevel(vol, None)

        # Draw circles and lines on fingers
        cv2.circle(image, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
        cv2.circle(image, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
        
    # Control video playback based on right hand position
    if right_hand_landmarks:
        # Extract coordinates of key points (fingers)
        x1, y1 = right_hand_landmarks[4][1:3]  # Thumb tip
        x2, y2 = right_hand_landmarks[8][1:3]  # Index finger tip
        x3, y3 = right_hand_landmarks[12][1:3]  # Middle finger tip
        x4, y4 = right_hand_landmarks[16][1:3]  # Ring finger tip
        x5, y5 = right_hand_landmarks[20][1:3]  # Little finger tip

        # Calculate distances between fingers
        distance_thumb_index = hypot(x2 - x1, y2 - y1)
        distance_index_middle = hypot(x3 - x2, y3 - y2)
        distance_middle_ring = hypot(x4 - x3, y4 - y3)
        distance_ring_little = hypot(x5 - x4, y5 - y4)
        
        # Check if all distances are greater than a threshold
        if (distance_thumb_index > 30 and distance_index_middle > 30 and
            distance_middle_ring > 30 and distance_ring_little > 30):
            # All fingers spread open (play gesture)
            if not is_playing:
                print("Play")
                is_playing = True
                # Start video playback in a separate thread
                threading.Thread(target=play_video).start()
        else:
            # All fingers are closer (fist gesture)
            if is_playing:
                print("Pause")
                is_playing = False
                # Pause video playback
                cap.release()  # Release video capture object

    return cv2.flip(image, 1)

def play_video():
    global is_playing
    cap = cv2.VideoCapture(video_path)
    while is_playing:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video", frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class VideoProcessor:
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = process(img)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    webrtc_ctx = webrtc_streamer(
        key="WYH",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=VideoProcessor,
        async_processing=True,
    )

if __name__ == "__main__":
    main()
