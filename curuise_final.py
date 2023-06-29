#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################
## Version2:
## 控制算法：检测一横线上的灰度突变位置，与标识点（绝对坐标固定）计算角度作为PID输入。

from driver import driver
import time
import cv2
import numpy as np
import math
from car_cam import img_process

class PID_Controller:
    def __init__(self,kp,ki,kd,output_min,output_max):

        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error = 0
        self.last_error = 0
        self.error_sum = 0
        self.error_diff = 0

        self.output_min = output_min
        self.output_max = output_max
        self.output = 0

    def constrain(self, output):

        if output > self.output_max:
            output = self.output_max
        elif output < self.output_min:
            output = self.output_min
        else:
            output = output
        return output

    def get_output(self, error):

        self.error = error
        self.error_sum += self.error
        self.error_diff = self.error - self.last_error
        self.last_error = self.error
        output = self.kp * self.error + self.ki * self.error_sum + self.kd * self.error_diff
        self.output = self.constrain(output)
        return self.output

def get_mid(flag,row):
    mid = 0
    if len(flag) >= 3:
        if len(flag) == 4:  # 0101
            print(flag[1][1], flag[2][1])
            mid = (flag[1][1] + flag[2][1]) / 2
        elif len(flag) == 3:
            if flag[0][0] == 1:  # 101
                print(flag[0][1], flag[1][1])
                mid = (flag[0][1] + flag[1][1]) / 2
            elif flag[0][0] == 0:  # 010
                print(flag[1][1], flag[2][1])
                mid = (flag[1][1] + flag[2][1]) / 2
        else:
            mid = 0
    elif len(flag) == 2:
        flag3 = []
        for i in range(img.shape[1] - 1):
            diff = int(img[row + 10][i + 1]) - int(img[row + 10][i])
            if diff > 100:  # 黑切白：1
                flag3.append([1, i])
            elif diff < -100:  # 白切黑：0
                flag3.append([0, i])
        if len(flag3) <= 2:
            if flag[0][1] - flag3[0][1] > 0:  # 左线
                mid = int((640 + flag[1][1]) / 2)
                print('Left Line!')
            else:
                mid = int(flag[0][1] / 2)
                print('Right Line!')
    else:
        mid = 0
    return mid

def Target_mid_select(row1,row2):
    mid_coordinate = 0
    sum_of_black = 0
    flag=[]
    row = 90
    # 记录黑线边缘的位置
    for i in range(img.shape[1] - 1):
        diff = int(img[row1][i + 1]) - int(img[row1][i])
        if int(img[row1][i]) == 0 :
            sum_of_black = sum_of_black + 1
        if diff > 100:  # 黑切白：1
            flag.append([1, i])
        elif diff < -100:  # 白切黑：0
            flag.append([0, i])
    
    if sum_of_black < 150 :
        print('row1')
        row = row1
        mid_coordinate = get_mid(flag,row)
    else :
        sum_of_black = 0
        for i in range(img.shape[1] - 1):
            diff = int(img[row2][i + 1]) - int(img[row2][i])
            if int(img[row2][i]) == 0 :
                sum_of_black = sum_of_black + 1
            if diff > 100:  # 黑切白：1
                flag.append([1, i])
            elif diff < -100:  # 白切黑：0
                flag.append([0, i])
        if sum_of_black < 150 :
            print('row2')
            row = row2
            mid_coordinate = get_mid(flag,row)
        else:
            row = 90
            mid_coordinate = 0

    print('mid', mid_coordinate)   
    return mid_coordinate,row  

if  __name__ == '__main__':
    print("==========piCar Client Start==========")
    d = driver()
    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="speed")
    b = True
    cap = cv2.VideoCapture(1)
    error_last = 0
    error = 0
    row1 = 90
    row2 = 160
    st = 0
    sm = 0
    servo_controller1 = PID_Controller(0.9, 0, 0, -0.8, 0.8)
    servo_controller2 = PID_Controller(0.8, 0, 0, -0.8, 0.8)
    while True:
        ret, frame = cap.read()
        if frame is None:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = img_process(gray)
        # 变量初始化
        setpoint = [250,320] #标志点
        mid,row = Target_mid_select(row1,row2)
        if row == row1 : 
            servo_controller = servo_controller1
        else:
            servo_controller = servo_controller2
        # 控制部分
        if mid > 0:
            if abs(mid- setpoint[1]) < 10:
                st = 0
                sm = 0.1
            else:
                error_last = error
                error = math.atan(float(mid - setpoint[1]) / float(row - setpoint[0]))
                print('error:', error)
                if error_last *  error < 0 and abs(error_last-error)>0.6:
                    sm = 0.05
                else:
                    st = servo_controller.get_output(error)
                    sm = 0.08
        else:
            sm = 0.05
        d.setStatus(motor=sm, servo=st)
        print("Motor: %0.2f, Servo: %0.2f" % (sm, st))
        time.sleep(0.2)
