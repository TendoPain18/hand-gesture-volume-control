import cv2
import mediapipe as mp
import fps


def draw_line_between_two_lm(img, lm_1, lm_2, cen_cir=False, cen_clr=(255, 0, 255)):
    if lm_1 and lm_2:
        cv2.line(img, (lm_1[0], lm_1[1]), (lm_2[0], lm_2[1]), (255, 0, 255), 3)
        if cen_cir:
            cx = (lm_1[0] + lm_2[0]) // 2
            cy = (lm_1[1] + lm_2[1]) // 2
            cv2.circle(img, (cx, cy), 15, cen_clr, cv2.FILLED)


class HandDetector:
    def __init__(self, mode=False, max_hands=2, complexity=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.complexity = complexity
        self.detectionCon = detection_con
        self.trackCon = track_con
        self.results = None
        self.mpDraw = None
        self.hands = None
        self.mpHands = None
        self.handFounded = False
        self.initialize_variables()

    def is_there_hand(self):
        return self.handFounded

    def initialize_variables(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def draw_hand(self, img, results, num):
        if results.multi_hand_landmarks[num]:
            hand = results.multi_hand_landmarks[num]
            self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)

    def draw_all_hands(self, img, results):
        if results.multi_hand_landmarks:
            for handLms in range(len(results.multi_hand_landmarks)):
                self.draw_hand(img, results, handLms)

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            self.handFounded = True
        else:
            self.handFounded = False
        if draw:
            self.draw_all_hands(img, self.results)

    def find_all_positions(self, img, hand_no=0, draw=True):
        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            for ID, ln in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(ln.x * w), int(ln.y * h)
                lm_list.append([ID, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return lm_list

    def find_position(self, img, hand_no=0, lm_no=0, draw=True):
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]
            h, w, c = img.shape
            ln = my_hand.landmark[lm_no]
            cx, cy = int(ln.x * w), int(ln.y * h)
            if draw:
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
            return [cx, cy]


def main():
    fps_ = fps.FPSCounter()
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        detector.find_hands(img)

        lm_list = detector.find_position(img, 0, 8)
        print(lm_list)

        fps_.display_fps(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
