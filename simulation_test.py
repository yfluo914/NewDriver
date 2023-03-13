# make sure other custom functions and libs can be imported under given path
import cv2
import numpy as np
import base64
import math

log = []
slow = 5

color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([80, 100, 120]), 'Upper': np.array([130, 220, 180])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'yellow': {'Lower': np.array([25, 160, 230]), 'Upper': np.array([45, 250, 255])},
              'white': {'Lower': np.array([0, 0, 221]), 'Upper': np.array([180, 30, 255])}}


def Crossing_detection2(view1):
    # 路口识别
    # 出口标志牌
    ori4 = view1
    thres1 = 11000
    thres2 = 700
    size4 = ori4.shape
    # print(size2)
    roi4 = ori4[int(355 / 575 * size4[0]):int(575 / 575 * size4[0]),
                int(260 / 1023 * size4[1]):int(480 / 1023 * size4[1])]
    blur4 = cv2.GaussianBlur(roi4, (5, 5), 0)
    hsv_img4 = cv2.cvtColor(blur4, cv2.COLOR_BGR2HSV)
    inRange_hsv4 = cv2.inRange(
        hsv_img4, color_dist['white']['Lower'], color_dist['white']['Upper'])
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv4 = cv2.erode(inRange_hsv4, kernel, iterations=1)
    kernel = np.ones((3, 3), dtype=np.uint8)
    inRange_hsv4 = cv2.dilate(erode_hsv4, kernel, iterations=3)
    sum_of_white1 = len((inRange_hsv4[inRange_hsv4 == 255]))

    roi5 = ori4[int(290 / 575 * size4[0]):int(525 / 575 * size4[0]),
                int(570 / 1023 * size4[1]):int(620 / 1023 * size4[1])]
    blur5 = cv2.GaussianBlur(roi5, (5, 5), 0)
    hsv_img5 = cv2.cvtColor(blur5, cv2.COLOR_BGR2HSV)
    inRange_hsv5 = cv2.inRange(
        hsv_img5, color_dist['white']['Lower'], color_dist['white']['Upper'])
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv5 = cv2.erode(inRange_hsv5, kernel, iterations=1)
    kernel = np.ones((3, 3), dtype=np.uint8)
    inRange_hsv5 = cv2.dilate(erode_hsv5, kernel, iterations=3)
    sum_of_white2 = len((inRange_hsv5[inRange_hsv5 == 255]))

    print('--', sum_of_white1, '--', sum_of_white2, '--')
    if sum_of_white1 >= thres1 and sum_of_white2 <= thres2:
        return 1
    return 0
    # cv2.imshow("ori4", ori4)
    # cv2.imshow("roi4", roi4)
    # cv2.imshow("hsv4", inRange_hsv4)


def image_to_speed(view1, view2, view3, view4, state):
    # global timer1,counter1

    view1 = cv2.imdecode(view1, cv2.IMREAD_ANYCOLOR)
    view2 = cv2.imdecode(view2, cv2.IMREAD_ANYCOLOR)
    view3 = cv2.imdecode(view3, cv2.IMREAD_ANYCOLOR)
    if state.get() is None:
        state.set(0)
    else:
        # print('case：'+str(state.get()))
        state.set(state.get()+1)
        if state.get() == 1:
            info_tim = open('timer1.txt', 'w')
            info_cnt = open('counter1.txt', 'w')
            info_stp = open('stop1.txt', 'w')
            info_tim.write('0')
            info_cnt.write('0')
            info_stp.write('0')
            info_tim.close()
            info_cnt.close()
            info_stp.close()

    info_tim = open('timer1.txt', 'r')
    info_cnt = open('counter1.txt', 'r')
    info_stp = open('stop1.txt', 'r')
    timer1 = info_tim.read()
    counter1 = info_cnt.read()
    stop1 = info_stp.read()
    info_tim.close()
    info_cnt.close()
    info_stp.close()
    timer1 = int(timer1)
    counter1 = int(counter1)
    stop1 = int(stop1)
    print('*', counter1, '*')

    if Crossing_detection2(view3) == 1:
        print('find crossing!')
        counter1 += 1
    if counter1 == 1:
        if timer1 <= 8:
            left_speed = right_speed = 2
        elif timer1 <= 21:
            left_speed = 2.2
            right_speed = 2
        else:
            left_speed = right_speed = 2
        timer1 += 1
    elif counter1 ==2 :
        timer1 = 0
        left_speed = right_speed = 3
    elif counter1 == 7:
        if timer1 <= 12:
            left_speed = right_speed = 2
        elif timer1 <= 25:
            left_speed = 2
            right_speed = 2.2
        else:
            left_speed = right_speed = 2
        timer1 += 1
     
    elif counter1 >= 8:
        left_speed = right_speed = 0
    else:
        left_speed = right_speed = 3

    if state.get() != 1:
        info_tim = open('timer1.txt', 'w')
        info_cnt = open('counter1.txt', 'w')
        info_stp = open('stop1.txt', 'w')
        info_tim.write(str(timer1))
        info_cnt.write(str(counter1))
        info_stp.write(str(stop1))
        info_tim.close()
        info_cnt.close()
        info_stp.close()

    # constant speed
    return left_speed, right_speed, 0, 0
