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
              'yellow2': {'Lower': np.array([25, 100, 230]), 'Upper': np.array([45, 180, 255])}}

def Stall_detection(view3):
    # 车位识别
    thres = 1000
    ori1 = view3
    size1 = ori1.shape
    roi1 = ori1[int(150 / 575 * size1[0]):int(500 / 575 * size1[0]), int(0 / 1023 * size1[1]):int(400 / 1023 * size1[1])]
    blur1 = cv2.GaussianBlur(roi1, (5, 5), 0)
    hsv_img1 = cv2.cvtColor(blur1, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv1 = cv2.erode(hsv_img1, kernel, iterations=1)
    inRange_hsv1 = cv2.inRange(erode_hsv1, color_dist['yellow']['Lower'], color_dist['yellow']['Upper'])
    sum_of_yellow = len((inRange_hsv1[inRange_hsv1 == 255]))
    #cv2.imshow("roi1", roi1)
    #cv2.imshow("hsv1", inRange_hsv1)
    #cv2.waitKey(500)
    print('sum_of_yellow',sum_of_yellow)
    #if sum_of_yellow > 0: print('sum_of_yellow',sum_of_yellow)
    if sum_of_yellow > thres:
        return 1
    return 0

def Crossing_detection(view2):
    # 路口识别
    # 出口标志牌
    # ori2=cv2.imread("./View218.jpg")
    flag1 = flag2 = 0
    thres1 = 350
    thres2 = 100 * 0.56
    ori2 = view2
    size2 = ori2.shape
    roi2 = ori2[int(0 / 575 * size2[0]):int(300 / 575 * size2[0]),
           int(750 / 1023 * size2[1]):int(850 / 1023 * size2[1])]
    blur2 = cv2.GaussianBlur(roi2, (5, 5), 0)
    hsv_img2 = cv2.cvtColor(blur2, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv2 = cv2.erode(hsv_img2, kernel, iterations=1)
    kernel = np.ones((3, 3), dtype=np.uint8)
    dilate_hsv2 = cv2.dilate(erode_hsv2, kernel, iterations=2)
    inRange_hsv2 = cv2.inRange(dilate_hsv2, color_dist['blue']['Lower'], color_dist['blue']['Upper'])
    sum_of_blue = len((inRange_hsv2[inRange_hsv2 == 255]))
    if sum_of_blue!=0:  print('sum_of_blue',sum_of_blue)
    if sum_of_blue >= thres1:
        flag1 = 1
    #cv2.imshow("roi2", roi2)
    #cv2.imshow("hsv2", inRange_hsv2)
    #cv2.waitKey(1000)

    # 地面黄线
    roi3 = ori2[int(300 / 575 * size2[0]):int(500 / 575 * size2[0]),
           int(700 / 1023 * size2[1]):int(1000 / 1023 * size2[1])]
    blur3 = cv2.GaussianBlur(roi3, (5, 5), 0)
    hsv_img3 = cv2.cvtColor(blur3, cv2.COLOR_BGR2HSV)
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv3 = cv2.erode(hsv_img3, kernel, iterations=2)
    kernel = np.ones((3, 3), dtype=np.uint8)
    dilate_hsv3 = cv2.dilate(erode_hsv3, kernel, iterations=1)
    inRange_hsv3 = cv2.inRange(dilate_hsv3, color_dist['yellow2']['Lower'], color_dist['yellow2']['Upper'])
    sum_of_white = len((inRange_hsv3[inRange_hsv3 == 255]))
    print(sum_of_white)
    if sum_of_white >= thres2:
        flag2 = 1
    # cv2.imshow("roi3", roi3)
    # cv2.imshow("hsv3", inRange_hsv3)

    if flag1 == 1 :
        return 1
    return 0

def Crossing_detection2(view1):
    # 路口识别
    # 出口标志牌
    ori4 = view1
    thres = 340
    size4 = ori4.shape
    # print(size2)
    roi4 = ori4[int(0 / 575 * size4[0]):int(250 / 575 * size4[0]),
           int(200 / 1023 * size4[1]):int(500 / 1023 * size4[1])]
    blur4 = cv2.GaussianBlur(roi4, (5, 5), 0)
    hsv_img4 = cv2.cvtColor(blur4, cv2.COLOR_BGR2HSV)
    inRange_hsv4 = cv2.inRange(hsv_img4, color_dist['blue']['Lower'], color_dist['blue']['Upper'])
    kernel = np.ones((3, 3), dtype=np.uint8)
    erode_hsv4 = cv2.erode(inRange_hsv4, kernel, iterations=1)
    kernel = np.ones((3, 3), dtype=np.uint8)
    inRange_hsv4 = cv2.dilate(erode_hsv4, kernel, iterations=3)
    sum_of_white = len((inRange_hsv4[inRange_hsv4 == 255]))
    print('--', sum_of_white, '--')
    if sum_of_white >= thres:
        return 1
    return 0
    # cv2.imshow("ori4", ori4)
    # cv2.imshow("roi4", roi4)
    # cv2.imshow("hsv4", inRange_hsv4)


# timer1 = 0
# counter1 = 0
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
            info_tim = open('timer1.txt','w')
            info_cnt = open('counter1.txt','w')
            info_stp = open('stop1.txt','w')
            info_tim.write('0')
            info_cnt.write('0')
            info_stp.write('0')
            info_tim.close()
            info_cnt.close()
            info_stp.close()
    
    info_tim = open('timer1.txt','r')
    info_cnt = open('counter1.txt','r')
    info_stp = open('stop1.txt','r')
    timer1 = info_tim.read()
    counter1 = info_cnt.read()
    stop1 = info_stp.read()
    info_tim.close()
    info_cnt.close()
    info_stp.close()
    #print('*', timer1, '*')
    #print('*', counter1, '*')
    timer1 = int(timer1)
    counter1 = int(counter1)
    stop1 = int(stop1)
    print('*', counter1, '*')
    if counter1 <= 2:
        if Crossing_detection(view1)==1:
            print('find crossing!')
            counter1 = counter1+1
            print('*', counter1, '*')
            if counter1 == 2:
                timer1 = 18
                counter1 = 3
    if counter1 ==4:
        if Stall_detection(view2) == 1:
            print('**Stall!**')
            counter1 = 10

    if timer1 == 0:
        left_speed = 1
        right_speed = 1
    else:
        print('timer1',timer1)
        left_speed = 1.15
        right_speed = 1
        timer1=timer1-1
        if timer1 == 0:
            counter1 = 4
    
    if counter1 >= 10 :
        print('**Back!**', counter1)
        left_speed=-1.1
        right_speed=-0.9
        counter1+=1
    if counter1 >= 23:
        print('**Back!**', counter1)
        left_speed=-1
        right_speed=-1
        counter1+=1
    if counter1 >= 40:
        print('**Back!**', counter1)
        left_speed=-1.1
        right_speed=-1
        counter1+=1
    if counter1 >= 60:
        print('**GO!**', counter1)
        left_speed=1.1
        right_speed=1
        counter1+=1
    if counter1 > 70: 
        left_speed=right_speed=0
    
    
    if state.get() != 1:
        info_tim = open('timer1.txt','w')
        info_cnt = open('counter1.txt','w')
        info_stp = open('stop1.txt','w')
        info_tim.write(str(timer1))
        info_cnt.write(str(counter1))
        info_stp.write(str(stop1))
        info_tim.close()
        info_cnt.close()
        info_stp.close()
    
    # constant speed
    return left_speed, right_speed
