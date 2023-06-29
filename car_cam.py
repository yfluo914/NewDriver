import numpy as np
import cv2
import os

# 加载灰度图像
def detect_black_region(image, threshold=0.5):
    """
    :param image (480,640)
    :return 是否监测到直线
    """
    # 二值化图像
    _, binary = cv2.threshold(image[430:480,:], 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    
    # 计算黑色像素总数
    total_black_pixels = cv2.countNonZero(binary)
    
    # 计算图像尺寸
    height, width = binary.shape
    
    # 计算黑色像素密度
    density = float(total_black_pixels) / (height * width)
    
    # 判断黑色像素密度是否大于阈值
    if density > threshold:
        return True
    
    return False


def countBlack(img,theresh=0.3):

    return img[0,-1]+img[-1,0]+img[-1,-1]+img[0,0]>255

def img_process(img,type='line',debug=False):
    """
    图像预处理
    :param img: 原始图像(480,640)
    :return: 处理后的图像(260,640)
    """
    blackBlock=[]
    if type=='line':
        img1 = img[220:350,:320]
        img2 = img[220:350,320:]
        img3 = img[350:480,:320]
        img4 = img[350:480,320:]

        

        # 二值化图像
        img_thresh1 = cv2.threshold(img1, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        img_thresh2 = cv2.threshold(img2, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        img_thresh3 = cv2.threshold(img3, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        img_thresh4 = cv2.threshold(img4, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        blackBlock=[countBlack(img_thresh1),countBlack(img_thresh2),
                    countBlack(img_thresh3),countBlack(img_thresh4)]
        img_thresh=np.zeros((260,640),dtype=np.uint8)

        img_thresh[:130,0:320]=img_thresh1
        img_thresh[:130,320:]=img_thresh2
        img_thresh[130:,0:320]=img_thresh3
        img_thresh[130:,320:]=img_thresh4

    elif type=='park':
        img1 = img[220:,:320]
        img2 = img[220:,320:]


        # 二值化图像
        img_thresh1 = cv2.threshold(img1, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        img_thresh2 = cv2.threshold(img2, 150, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        img_thresh=np.zeros((260,640),dtype=np.uint8)

        img_thresh[:,0:320]=img_thresh1
        img_thresh[:,320:]=img_thresh2


    if debug:
        cv2.imshow('src', img_thresh)
        # cv2.waitKey(0)
        
    if type=='line':
        kernel = np.ones((5, 5), dtype=np.uint8)
        img_ero = cv2.erode(img_thresh, kernel, iterations=1)
        img_dil= cv2.dilate(img_ero, kernel, iterations=1)
        img_ero = cv2.erode(img_dil, kernel, iterations=2)
        img_dil= cv2.dilate(img_ero, kernel, iterations=3)
        img_ero = cv2.erode(img_dil, kernel, iterations=1)

        return img_ero,blackBlock
    elif type=='park':
        kernel = np.ones((5, 5), dtype=np.uint8)
        img_ero = cv2.erode(img_thresh, kernel, iterations=5)


        return img_ero

    # kernel1 = np.ones((5, 5), dtype=np.uint8)
    # kernel2 = np.ones((20, 20), dtype=np.uint8)
    # img_ero = cv2.erode(img_thresh, kernel1, iterations=1)
    # img_dil= cv2.dilate(img_ero, kernel1, iterations=2)
    # img_ero = cv2.erode(img_dil, kernel1, iterations=2)
    # img_dil= cv2.dilate(img_ero, kernel1, iterations=3)
    # img_ero = cv2.erode(img_dil, kernel2, iterations=3)
    # img_dil= cv2.dilate(img_ero, kernel2, iterations=3)
if __name__=="__main__":
    folder='pic'
    input_path = os.path.join(folder,'input')
    output_path = os.path.join(folder,'output')
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
        print(f"Create folder '{output_path}' successfully!")
    for filename in os.listdir(input_path):
        if filename.endswith('.jpg'):
            print(filename)
            img=cv2.imread(os.path.join(input_path,filename), cv2.IMREAD_GRAYSCALE)

            img_p,l=img_process(img) 
            print(l)

            path = os.path.join(output_path, filename)
            cv2.imwrite(path, img_p)

# cv2.imshow('erode', img_dil)
# cv2.waitKey(0)
# print(img_ero)