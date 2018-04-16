'''
This file is to draw the puzzle boxes

'''

import cv2


def grid(img):
    cv2.rectangle(img, (100, 50), (200, 150), (0, 255, 0), 0)
    cv2.rectangle(img, (200, 50), (300, 150), (0, 255, 0), 0)
    cv2.rectangle(img, (150, 150), (250, 250), (0, 255, 0), 0)
    cv2.rectangle(img, (100, 250), (200, 350), (0, 255, 0), 0)
    cv2.rectangle(img, (200, 250), (300, 350), (0, 255, 0), 0)
    cv2.rectangle(img, (450, 150), (600, 300), (255, 255, 0), 0)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while (cap.isOpened()):
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        grid(img)

        cv2.namedWindow('Gesture', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Gesture', 1000, 1000)
        # cv2.setWindowProperty("Gesture", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Gesture', img)
        k = cv2.waitKey(10)
        if k == 27:
            break
