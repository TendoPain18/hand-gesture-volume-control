import datetime
import cv2


class FPSCounter:
    def __init__(self):
        self.p_time = datetime.datetime.now()
        self.fps = 0
        self.counter = 0

    def calculate_fps(self):
        current_time = datetime.datetime.now()
        if current_time < self.p_time + datetime.timedelta(seconds=1):
            self.counter += 1
        else:
            self.fps = self.counter
            self.counter = 0
            self.p_time = current_time
        return self.fps

    def display_fps(self, img):
        self.calculate_fps()
        cv2.putText(img, "FPS: " + str(self.fps), (10, 40), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 0, 0), 3)


def main():
    fps = FPSCounter()
    while True:
        print(fps.calculate_fps())


if __name__ == "__main__":
    main()
