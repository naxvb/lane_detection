import numpy as np
import cv2

vid = cv2.VideoCapture(1)
c=0
 
ret, frame = vid.read()
roi=[0,0,frame.shape[1],frame.shape[0]] #x - frame[1] = 640, y - frame[0] = 360

while True:
    ret, frame = vid.read()
    # obraz obrobka
    cv2.imshow('frame', frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
    #cv2.imshow("ROI", image)
    
    c = cv2.waitKey(1) 
    if c == ord('q'):
        break

    roi = [200, 150, frame.shape[1], frame.shape[0]]

    roi_cropped = hsv[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])] #najpierw y potem x 
    th3 = cv2.adaptiveThreshold(roi_cropped,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 191, 5)
    #print(th3.shape[1],th3.shape[0])
    sumX = 0
    sumY = 0
    old_meanX = 0
    old_meanY = 0
    count = 0
    for i in range(int(roi[1])-50, roi_cropped.shape[0]):
        for j in range(int(roi[0])-50, roi_cropped.shape[1]):
            if th3[i,j] == 0:
                sumX = sumX + i
                sumY = sumY + j
                count = count + 1
                meanX = sumX / count
                meanY = sumY / count
                old_meanX = meanX
                old_meanY = meanY
            else:
                meanX = old_meanX
                meanY = old_meanY    
    meanX = int(meanX)
    meanY = int(meanY)
    start_point = (meanY, meanX)#(200, 300) # X, Y
    end_point = (meanY+5, meanX+5) #(300, 640)
    bandbox = cv2.rectangle(th3, start_point, end_point, (255,255,255), 5) #kropka na linii toru
    print(meanX, meanY)
    # ref_start_point = (int(roi_cropped.shape[1]/2) +50,  int(roi_cropped.shape[0]/2)+50)
    # ref_end_point =  (5 + int(roi_cropped.shape[1]/2) +50, 5 + int(roi_cropped.shape[0]/2)+50)
    ref_start_point = (283,  int(roi[1]))
    ref_end_point =  (283,  5 + int(roi[1]))
    ref = cv2.rectangle(th3, ref_start_point,ref_end_point, (0,0,0), 5) # kropka referencyjna

    diff = meanX - int(roi[1])
    print(diff)
   
    cv2.imshow("ROI", th3)

vid.release()
cv2.destroyAllWindows()
