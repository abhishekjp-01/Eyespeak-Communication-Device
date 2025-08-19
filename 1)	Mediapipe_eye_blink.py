import cv2
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2
import JPOledMenu
import time

start_time = None

# Setup Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(1)

# Setup Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Eye landmarks (left and right eye)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def get_ear(landmarks, eye_points, image_w, image_h):
    p = [landmarks[i] for i in eye_points]
    p = [(int(pt.x * image_w), int(pt.y * image_h)) for pt in p]
    ear = (euclidean(p[1], p[5]) + euclidean(p[2], p[4])) / (2.0 * euclidean(p[0], p[3]))
    return ear

JPOledMenu.boot_logo()
JPOledMenu.draw_menu()
start_time = None
mode_select = True
time.sleep(1)
while True:
    
    frame = picam2.capture_array()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    h, w, _ = frame.shape
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            ear_left = get_ear(face_landmarks.landmark, LEFT_EYE, w, h)
            ear_right = get_ear(face_landmarks.landmark, RIGHT_EYE, w, h)

            if mode_select == True:
                if ear_left < 0.20 and ear_right >=0.20:
                    if start_time is None:
                        start_time = time.time()
                    elif (time.time()-start_time) >= 0.3:
                        JPOledMenu.scroll_up()
                        start_time = None
                    
                elif ear_right < 0.20 and ear_left >=0.20:
                    if start_time is None:
                        start_time = time.time()
                    elif (time.time()-start_time) >= 0.3:
                        JPOledMenu.scroll_down()
                        start_time = None
        
                elif ear_right < 0.20 and ear_left < 0.20:
                    if start_time is None:
                        start_time = time.time()
                    elif (time.time()-start_time) >= 0.3:
                        JPOledMenu.select()
                        start_time = None
                else:
                    start_time = None
            
            else:
                if ear_left < 0.20 and ear_right >=0.20:
                    if start_time is None:
                        start_time = time.time()
                    elif (time.time()-start_time) >= 2:
                        menu_select = True
                        start_time = None
                        
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
            
cv2.destroyAllWindows()

