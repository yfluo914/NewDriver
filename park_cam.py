import numpy as np
import cv2
import os
import glob
import math
from car_cam import img_process


mtx=np.array([[432.43449925,0,313.90085725],[0,420.82585648,261.48247235],[0,0,1]])
dist=np.array([-0.57440594,0.59185263,-0.02762762,0.00526766,-0.33835946])
M=np.array([[ 1.62485103e+00,  4.75799468e+00, -3.78603206e+02],
 [ 1.44251243e-01 , 1.18771852e+01 ,-1.64611020e+02],
 [ 6.13835075e-04 , 3.81290060e-02 , 1.00000000e+00]])

def park_coord(img,debug=False):
    undistorted_frame = cv2.undistort(img, mtx, dist)

    # Edge detection
    #dst = cv2.Canny(fname_p, 50, 200, None, 3)
    dst = cv2.Canny(undistorted_frame[260:,:], 50, 200, None, 3)
    dst = cv2.warpPerspective(dst, M, (250,400))[:300,60:190]
    
    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    
    cdstP = np.copy(cdst)
    

    # Probabilistic Line Transform
    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 20, None, 50, 10)

    # Draw the lines
    minx=250
    mini=0
    maxx=0
    maxi=0
    if linesP is not None:
        for i in range(0, len(linesP)):
            x1,y1,x2,y2 = linesP[i][0]
            print(linesP[i][0])
            if (x2-x1==0 and abs(y2-y1)>5) or abs((y2-y1)/(x2-x1))>8:
                if min(x1,x2)<minx:
                    minx=min(x1,x2)
                    mini=i
                if max(x1,x2)>maxx:
                    maxx=max(x1,x2)
                    maxi=i
                
    
    midx=(linesP[mini][0][0]+linesP[mini][0][2]+linesP[maxi][0][0]+linesP[maxi][0][2])/4
    midy=(min(linesP[mini][0][1],linesP[mini][0][3])+min(linesP[maxi][0][1],linesP[maxi][0][3]))/2
    angle=(math.atan2(linesP[mini][0][3]-linesP[mini][0][1],linesP[mini][0][2]-linesP[mini][0][0])
           +math.atan2(linesP[maxi][0][3]-linesP[maxi][0][1],linesP[maxi][0][2]-linesP[maxi][0][0]))/2
    
    if debug:
        cv2.line(cdstP, (linesP[mini][0][0], linesP[mini][0][1]), (linesP[mini][0][2], linesP[mini][0][3]), (0,0,255), 3, cv2.LINE_AA)
        cv2.line(cdstP, (linesP[maxi][0][0], linesP[maxi][0][1]), (linesP[maxi][0][2], linesP[maxi][0][3]), (0,0,255), 3, cv2.LINE_AA)
        cdstP=cv2.circle(cdstP, (int(midx),int(midy)), 5, (255,255,255), -1)
        print((midx,midy), angle)
        return cdstP
    return (midx,midy), angle

if __name__=='__main__':
    folder='parking'
    input_path = os.path.join('input',folder)
    output_path = os.path.join('output',folder)
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
        print(f"Create folder '{output_path}' successfully!")
    for filename in os.listdir(input_path):
        if filename.endswith('.jpg'):
            print(filename)
            img=cv2.imread(os.path.join(input_path,filename), cv2.IMREAD_GRAYSCALE)

            img_p=park_coord(img,debug=True) 

            path = os.path.join(output_path, filename)
            cv2.imwrite(path, img_p)



