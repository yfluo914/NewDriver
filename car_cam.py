import numpy as np
import cv2
import os

# 加载灰度图像

input_path = 'pic2'
output_path = 'output'
for i in range(0, 41):
    pathi='%s.jpg'%i
    path = os.path.join(input_path, pathi)
    img1 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)[220:350,:320]
    img2 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)[220:350,320:]
    img3 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)[350:480,:320]
    img4 = cv2.imread(path, cv2.IMREAD_GRAYSCALE)[350:480,320:]

    # 二值化图像
    img_thresh1 = cv2.threshold(img1, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    img_thresh2 = cv2.threshold(img2, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    img_thresh3 = cv2.threshold(img3, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    img_thresh4 = cv2.threshold(img4, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
    img_thresh=np.zeros((260,640),dtype=np.uint8)

    img_thresh[:130,0:320]=img_thresh1
    img_thresh[:130,320:]=img_thresh2
    img_thresh[130:,0:320]=img_thresh3
    img_thresh[130:,320:]=img_thresh4
    cv2.imshow('thresh', img_thresh)
    # cv2.waitKey(0)

    kernel = np.ones((5, 5), dtype=np.uint8)
    img_ero = cv2.erode(img_thresh, kernel, iterations=1)
    img_dil= cv2.dilate(img_ero, kernel, iterations=1)
    img_ero = cv2.erode(img_dil, kernel, iterations=2)
    img_dil= cv2.dilate(img_ero, kernel, iterations=3)
    img_ero = cv2.erode(img_dil, kernel, iterations=1)

    # kernel1 = np.ones((5, 5), dtype=np.uint8)
    # kernel2 = np.ones((20, 20), dtype=np.uint8)
    # img_ero = cv2.erode(img_thresh, kernel1, iterations=1)
    # img_dil= cv2.dilate(img_ero, kernel1, iterations=2)
    # img_ero = cv2.erode(img_dil, kernel1, iterations=2)
    # img_dil= cv2.dilate(img_ero, kernel1, iterations=3)
    # img_ero = cv2.erode(img_dil, kernel2, iterations=3)
    # img_dil= cv2.dilate(img_ero, kernel2, iterations=3)

    path = os.path.join(output_path, pathi)
    print(path)
    cv2.imwrite(path, img_ero )

# cv2.imshow('erode', img_dil)
# cv2.waitKey(0)
# print(img_ero)