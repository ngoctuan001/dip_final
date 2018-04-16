'''

This file is to detect the hand gesture
'''

import cv2
import numpy as np
import math
from detect_fist_temp import detect_fist_without_drawing


class hand_:
    def __init__(self):
        self.lower = np.array([0, 48, 80], dtype="uint8")
        self.upper = np.array([20, 255, 255], dtype="uint8")
        self.skin_detection_array = []
        self.skin_detection_temp = False
        self.skin_detection_final = False

    def hand_gesture(self, screen):

        while (1):

            crop_img = screen

            # ----------------- This block is to detect skin----------------- #
            frame = screen

            # and determine the HSV pixel intensities that fall into
            # the speicifed upper and lower boundaries
            converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            skinMask = cv2.inRange(converted, self.lower, self.upper)

            # apply a series of erosions and dilations to the mask
            # using an elliptical kernel
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
            skinMask = cv2.erode(skinMask, kernel, iterations=2)
            skinMask = cv2.dilate(skinMask, kernel, iterations=2)

            # blur the mask to help remove noise, then apply the
            # mask to the frame
            skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
            skin = cv2.bitwise_and(frame, frame, mask=skinMask)

            # show the skin in the image along with the mask

            if skin.any():

                self.skin_detection_temp = True
                self.skin_detection_final = True
                self.skin_detection_array.clear()
                print("Found Skin " + str(self.skin_detection_temp) + " and len is " + str(
                    self.skin_detection_array) + " and final is" + str(self.skin_detection_final))
            else:
                self.skin_detection_temp = False
                self.skin_detection_array.append(0)
                print("No Skin " + str(self.skin_detection_temp) + " and len is " + str(
                    self.skin_detection_array) + " and final is" + str(self.skin_detection_final))
                if (len(self.skin_detection_array)) > 15:
                    self.skin_detection_final = False
                    print("No Skin " + str(self.skin_detection_temp) + " and len is " + str(
                        len(self.skin_detection_array)) + " and final is" + str(self.skin_detection_final))
                    if (len(self.skin_detection_array)) > 50:
                        self.skin_detection_array.clear()
                        print("Clear Stack")

            # ----------------- This block is to detect gesture base on grayscale ----------------- #

            # convert to grayscale
            grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            cv2.imshow('greayscale', grey)
            # applying gaussian blur
            value = (25, 25)
            blurred = cv2.GaussianBlur(grey, value, 0)

            # thresholdin: Otsu's Binarization method
            _, thresh1 = cv2.threshold(blurred, 127, 255,
                                       cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            thresh1 = cv2.erode(thresh1, None, iterations=2)
            thresh1 = cv2.dilate(thresh1, None, iterations=2)
            # show thresholded image
            cv2.imshow('Thresholded', thresh1)

            # check OpenCV version to avoid unpacking error
            (version, _, _) = cv2.__version__.split('.')

            if version == '3':
                image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
                                                              cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            elif version == '2':
                contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, \
                                                       cv2.CHAIN_APPROX_NONE)

            # find contour with max area
            cnt = max(contours, key=lambda x: cv2.contourArea(x))

            # create bounding rectangle around the contour (can skip below two lines)
            # x, y, w, h = cv2.boundingRect(cnt)
            # cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)

            # finding convex hull
            hull = cv2.convexHull(cnt)

            # drawing contours
            drawing = np.zeros(crop_img.shape, np.uint8)
            cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)

            # finding convex hull
            hull = cv2.convexHull(cnt, returnPoints=False)

            hull_for_drawing = cv2.convexHull(cnt)

            hull_start = tuple(hull_for_drawing[0][0])
            temp = tuple(hull_for_drawing[0][0])
            # hull_stop=tuple(hull_for_drawing[-1][0])
            # print('start')
            # print(hull_start)
            # print('stop')
            # print(hull_stop)
            # print(hull_for_drawing)
            # cv2.circle(crop_img, hull_start, 5, [255, 255, 255], -1)
            # cv2.circle(crop_img, hull_stop, 5, [0, 0, 0], -1)
            for item in hull_for_drawing:
                tuple_item = tuple(item[0])
                length_check = math.sqrt((tuple_item[0] - temp[0]) ** 2 + (tuple_item[1] - temp[1]) ** 2)
                if (length_check > 80):
                    temp = tuple_item
                    cv2.circle(crop_img, tuple_item, 5, [255, 255, 255], -1)

            # cv2.circle(crop_img,hull_for_drawing , 5, [51, 204, 51], -1)
            # finding convexity defects
            defects = cv2.convexityDefects(cnt, hull)
            count_defects = 0
            cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

            # applying Cosine Rule to find angle for all defects (between fingers)
            # with angle > 90 degrees and ignore defects
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]

                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])

                # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)

                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

                # apply cosine rule here
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                # ignore angles > 90 and highlight rest with red dots
                if angle <= 90:
                    count_defects += 1
                    cv2.circle(crop_img, far, 5, [0, 0, 255], -1)
                    # print (far)
                    cv2.circle(crop_img, start, 5, [0, 0, 204], -1)
                    cv2.circle(crop_img, end, 5, [51, 204, 51], -1)

                # dist = cv2.pointPolygonTest(cnt,far,True)

                # draw a line from start to end i.e. the convex points (finger tips)
                # (can skip this part)
                cv2.line(crop_img, start, end, [0, 255, 0], 2)
                # cv2.circle(crop_img,far,5,[0,0,255],-1)

            # ----------------- This block is to define action after recognition process----------------- #

            if not self.skin_detection_final:
                return "0"
            else:
                if count_defects == 1:
                    return "2"
                elif count_defects == 2:
                    return "3"
                elif count_defects == 3:
                    return "4"
                elif count_defects == 4:
                    return "5"
                else:
                    isFist = detect_fist_without_drawing(screen)
                    if not isFist:
                        return "1"
                    else:
                        return "0"


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    Test = hand_()
    while (cap.isOpened()):
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.rectangle(img, (450, 150), (600, 300), (255, 255, 0), 0)
        screen = img[150:300, 450:600]

        answer = Test.hand_gesture(screen)
        # print (answer)
        cv2.putText(img, answer, (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, 5)

        # cv2.namedWindow('Gesture', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('Gesture', 1000, 1000)
        # cv2.setWindowProperty("Gesture", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow('Gesture', img)
        k = cv2.waitKey(10)
        if k == 27:
            break
