'''

This is the main file

'''

import cv2
from grid import grid
import detect_fist_period
import hand_detect_class

# store answer and helper
flaglist = [0, 0, 0, 0, 0]
final_answer = [0, 0, 0, 0, 0]


# if there is a fist inside , put Text and update answer
def is_Fist(i, img, answer, confirm, flaglist, final_answer, center, a):
    isFist = a.detect(confirm, img)
    cv2.putText(img, answer, (500, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    if isFist:
        flaglist[i] = True
        cv2.putText(img, "Activated", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        cv2.putText(img, answer, center, cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        final_answer[i] = answer
    else:
        if flaglist[i] == True:
            cv2.putText(img, final_answer[i], center, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)


# open camera
cap = cv2.VideoCapture(0)

# create instance of class stack
a1 = detect_fist_period.detect_fist_during_time()
a2 = detect_fist_period.detect_fist_during_time()
a3 = detect_fist_period.detect_fist_during_time()
a4 = detect_fist_period.detect_fist_during_time()
a5 = detect_fist_period.detect_fist_during_time()

# create instance of class hand_detect_class
detect_box = hand_detect_class.hand_()

# open camera and run main function
while (cap.isOpened()):
    # # read image

    ret, img = cap.read()
    img = cv2.flip(img, 1)

    # draw 5 box of puzzle on left side
    grid(img)

    # locate the box of detecting hand
    screen = img[150:300, 450:600]

    # locate the boxes where to confirm isFist inside
    confirm_d0 = img[50:150, 100:200]
    confirm_d1 = img[50:150, 200:300]
    confirm_m = img[150:250, 150:250]
    confirm_y1 = img[250:350, 100:200]
    confirm_y2 = img[250:350, 200:300]

    # pass the box of detecting hand inside this function to get the answer
    answer = detect_box.hand_gesture(screen)

    # pass the paramaters in this function to confirm fist and putText inside that box
    is_Fist(0, img, answer, confirm_d0, flaglist, final_answer, (135, 125), a1)
    is_Fist(1, img, answer, confirm_d1, flaglist, final_answer, (235, 125), a2)
    is_Fist(2, img, answer, confirm_m, flaglist, final_answer, (185, 225), a3)
    is_Fist(3, img, answer, confirm_y1, flaglist, final_answer, (135, 325), a4)
    is_Fist(4, img, answer, confirm_y2, flaglist, final_answer, (235, 325), a5)

    # checking the answer
    print(final_answer)
    if final_answer == ['2', '3', '4', '4', '2']:
        print("Correct answer")
        cv2.putText(img, "ANSWER CORRECT", (150, 450), cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 255),
                    thickness=3)

    # make window full size
    cv2.namedWindow('Gesture', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('Gesture', 1000, 1000)
    cv2.setWindowProperty("Gesture", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('Gesture', img)

    # exit key
    k = cv2.waitKey(10)
    if k == 27:
        break
