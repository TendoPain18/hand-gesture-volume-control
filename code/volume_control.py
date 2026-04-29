import cv2
import screen_brightness_control as sbc
import fps
import hand_tracking
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_factor(img):
    [x1, y1] = detector.find_position(img, 0, 0, False)
    [x2, y2] = detector.find_position(img, 0, 5, False)
    length = math.hypot(x2 - x1, y2 - y1)

    factor = 1800 / length
    return factor


def map_range(x, x_min, x_max, y_min, y_max):
    mapped_value = y_min + (x - x_min) / (x_max - x_min) * (y_max - y_min)
    return max(min(mapped_value, y_max), y_min)


############################################
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
############################################

# detector = hand_tracking.HandDetector()

cap = cv2.VideoCapture(0)
fps_ = fps.FPSCounter()
detector = hand_tracking.HandDetector(detection_con=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol, maxVol, delta = volume.GetVolumeRange()

while True:
    success, img = cap.read()
    detector.find_hands(img)

    if detector.is_there_hand():
        f = get_factor(img)

        ebham = [x1, y1] = detector.find_position(img, 0, 4)
        sbaba = [x2, y2] = detector.find_position(img, 0, 8)

        length = (math.hypot(x2 - x1, y2 - y1) * f)

        # print(length)
        if length < 50:
            hand_tracking.draw_line_between_two_lm(img, ebham, sbaba, True, (0, 255, 0))
        else:
            hand_tracking.draw_line_between_two_lm(img, ebham, sbaba, True)

        smooth = 5
        vol = map_range(length, 450, 2550, 0, 100)
        vol = round(vol/smooth) * smooth
        # print(vol)
        volume.SetMasterVolumeLevelScalar(vol/100, None)
        # sbc.set_brightness(vol)


    fps_.display_fps(img)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
