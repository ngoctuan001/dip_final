'''

This file is to detect if the fist is inside the area for 0.2 seconds. This to avoid the confusing when we move the hand across many boxes

'''

import cv2
from detect_fist_temp import detect_fist

import time


class detect_fist_during_time:
    def __init__(self):
        self.first_fist_detection = False
        self.isFist = 0
        self.current_time = 0
        self.target_time = 0

    def detect(self, confirm, img):
        self.isFist = detect_fist(confirm)  # a function to detect fist inside that box

        self.current_time = int(time.time())

        if self.isFist and not self.first_fist_detection:
            self.first_fist_detection = True
            self.target_time = self.current_time + 0.2
        elif self.isFist and self.first_fist_detection:
            if self.current_time > self.target_time:
                cv2.putText(img, "Fist", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
                return True
        else:
            # that is, no fist is detected
            self.first_fist_detection = False
            return False
