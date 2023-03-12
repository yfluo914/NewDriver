import sys
import math
import numpy as np
import cv2

## 获取mask，区分出车道线所在的小区域
# 读取图像并转换为灰度图像
image = cv2.imread('View3.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)[260:420, :]

# 应用阈值化函数，将图像转换为二进制形式
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# 查找连通分量
connectivity = 8  # 8领域连接
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)

# 输出连通分量的数量
print(f"Number of connected components: {num_labels - 1}")  # 减去背景
whratio = 1
rec_i = 0
for i in range(1, num_labels):
    print(i, stats[i])
    if stats[i][2] > 70 and stats[i][2] / stats[i][3] > whratio:
        whratio = stats[i][2] / stats[i][3]
        rec_i = i
# 可以绘制标记的联通分量，使用以下代码
# img_with_labels = cv2.applyColorMap(labels.astype(np.uint8)*30, cv2.COLORMAP_JET)
# rec_i=5
# print(rec_i)
mask = (labels == rec_i)
# print(mask.shape)
mask_=np.zeros((image.shape[0],image.shape[1]),dtype=np.uint8)
# print(mask_.dtype)
mask_[260:420, :] = mask

## 用霍夫变换进行直线检测，获取theta、d参数
# Loads an image
src = cv2.imread('view3.jpg', cv2.IMREAD_GRAYSCALE) * mask_

# Check if image is loaded fine
if src is None:
    print('Error opening image!')
    print('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')

dst = cv2.Canny(src, 50, 200, None, 3)

# Copy edges to the images that will display the results in BGR
cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
cdstP = np.copy(cdst)

lines = cv2.HoughLines(dst, 1, np.pi / 180, 600)

print("检测到的直线参数",lines)  #由于车道线有一定宽度，检测结果可能为两条直线
# print(lines.dtype)
if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
        cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)

# linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, 10)
# if linesP is not None:
#     for i in range(0, len(linesP)):
#         l = linesP[i][0]
#         cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv2.LINE_AA)

cv2.imshow("Source", src)
cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
# cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

cv2.waitKey(0)

