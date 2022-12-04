#1: Inicjalizacja bibliotek
from jetcam.csi_camera import CSICamera
import ipywidgets
import matplotlib.pyplot as plt
from IPython import display
import cv2
import numpy as np
from jetracer.nvidia_racecar import NvidiaRacecar

car = NvidiaRacecar() 

# kamera
camera = CSICamera(width=224, height=224, capture_fps=65) #Jeżeli kamera jest już zainicjalizowana, to należy to zakomentować
camera.running = True

c = 0

frame = camera.value
roi=[0,0,frame.shape[1],frame.shape[0]]

roiR=[frame.shape[1]/2,frame.shape[0]/2,frame.shape[1],frame.shape[0]]
roiL=[0,frame.shape[0]/2,frame.shape[1]/2,frame.shape[0]]

steer=0
car.throttle = -0.6
car.steering = steer
lineLerr=0
lineRerr=0

while True:
    frame = camera.value
    # obraz obrobka
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray,15)
    grayL = gray[int(roiL[1]):int(roiL[1]+roiL[3]), int(roiL[0]):int(roiL[0]+roiL[2])]
    grayR = gray[int(roiR[1]):int(roiR[1]+roiR[3]), int(roiR[0]):int(roiR[0]+roiR[2])]

    th3 = cv2.adaptiveThreshold(grayL,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    th3 = cv2.Canny(th3, 75, 150)
    lines = cv2.HoughLines(th3,1,np.pi/180,20)

    if lines is not None:
        if lines[0][0][1]>0.48:
            lineLerr=lines[0][0][1]-0.48
    else:
        lineLerr=0

    th3 = cv2.adaptiveThreshold(grayR,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    th3 = cv2.Canny(th3, 75, 150)
    lines = cv2.HoughLines(th3,1,np.pi/180,20)

    if lines is not None:
        if lines[0][0][1]<2.7:
            lineRerr=2.7-lines[0][0][1]
    else:
        lineRerr=0

    control=lineRerr-lineLerr
    steer=5*control
    if steer>1:
        steer=1
    if steer<-1:
        steer=-1


    if lines is not None:
        #print(lines)
        cv2.putText(img=th3, text=str(lines[0][0][1]), org=(40, 40), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(255),thickness=1)

    car.steering = steer


    #plt.imshow(th3)
    #display.display(plt.gcf())
    #display.clear_output(wait=True)

    #plt.imshow(th3)
    #display.display(plt.gcf())
    #display.clear_output(wait=True) 
