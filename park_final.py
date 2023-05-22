#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################


from driver import driver
import time
import cv2
import numpy as np
import math
from car_cam import img_process
from park_cam import park_coord

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
        # print('error.sum',self.error_sum)
        return self.output

if  __name__ == '__main__':
    print("==========piCar Client Start==========")
    n = 2 #choose park position
    
    d = driver()
    d.setStatus(motor=0.0, servo=0.0, dist=0x00, mode="speed")
    b = True
    cap = cv2.VideoCapture(0)
    error_last = 0
    error = 0
    st = 0
    sm = 0
    servo_controller = PID_Controller(2, 0, 0, -0.8, 0.8)
    # 根据车位号选择前近距离
    t = [2.4,4.2,5.9,7.7]
    print('Go!')
    d.setStatus(motor=0.1,servo=0)
    time.sleep(t[n-1])
    # 转90度
    print('Turning 90 degrees')
    d.setStatus(motor=0.1,servo=1)
    time.sleep(3.5)
    # parking
    while True:
        ret, frame = cap.read()
        if frame is None:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 变量初始化
        setpoint = [260,75] #标志点
        
        (midx, midy), theta = park_coord(gray,debug=False)
        print('coord:',midx,midy)
        #cdst = park_coord(gray,debug=True)
        #cv2.imshow('cdst',cdst)
        # 控制部分
        if midy < 170:
            if abs(midy- setpoint[1]) < 3:
                st = 0
                sm = -0.02
            else:
                error_last = error
                error = -math.atan(float(midx - setpoint[1]) / float(midy-setpoint[0]))
                print('error:', error)
                if error_last *  error < 0 and abs(error_last-error)>0.3:
                    sm = -0.02
                else:
                    st = servo_controller.get_output(error)
                    sm = -0.02
            d.setStatus(motor=sm, servo=st)
        else:
            print('stop!')
            break
        print("Motor: %0.2f, Servo: %0.2f" % (sm, st))
        time.sleep(0.4)
        
    # back
    print('Back!')
    d.setStatus(motor=-0.03,servo=0)
    time.sleep(7.3)  
    d.setStatus(motor=0, servo=0,mode='stop')
