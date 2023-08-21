import cv2
import HandTrackingModule as htm
import numpy as np

cam=cv2.VideoCapture(0)

detector=htm.handDetector()


draw_color=(0,0,255)
img_canvas=np.zeros((720,1280,3),np.uint8)

while True:

    success,frame=cam.read()
    img=cv2.resize(frame,(1280,720))
    img=cv2.flip(img,1)

 #draw rectangle   
    cv2.rectangle(img,(0,50),(100,150),color=(255,255,255),thickness=-1)
    cv2.rectangle(img,(100,50),(200,150),color=(0,255,0),thickness=-1)
    cv2.rectangle(img,(200,50),(300,150),color=(255,0,0),thickness=-1)
    cv2.rectangle(img,(300,50),(400,150),color=(0,0,255),thickness=-1)
    cv2.rectangle(img,(400,50),(500,150),color=(255,255,0),thickness=-1)
    cv2.putText(img,text="ERASER",org=(10,100),fontFace=cv2.FONT_HERSHEY_DUPLEX,fontScale=0.70,color=(0,0,0),thickness=2)

 #find hands
    img=detector.findHands(img) 
    lmlist=detector.findPosition(img)
    # print(lmlist)  
    if len(lmlist)!=0:

        x1,y1=lmlist[8][1:]
        x2,y2=lmlist[12][1:]
        # print(x1,y1)

    #check if finger is up
        fingers=detector.fingersUp()
        print(fingers)   

    #selection mode index and middle finger is up
        if fingers[1] and fingers[2]:
            print("selection mode")
            xp,yp=0,0

            if y1<150:
                if 0 < x1 < 100:
                    print('eraser')
                    draw_color=(0,0,0)
                if 100 < x1 < 200:
                    print('green') 
                    draw_color=(0,255,0)
                if 200 < x1 < 300:
                    print('blue') 
                    draw_color=(255,0,0)
                if 300 < x1 < 400:
                    print('red') 
                    draw_color=(0,0,255)
                if 400 < x1 < 500:
                    print('light blue')  
                    draw_color=(255,255,0)  

            cv2.rectangle(img,(x1,y1),(x2,y2),draw_color,cv2.FILLED)                     



    #drawing mode only index finger is up
        if (fingers[1] and not fingers[2]):
            print("drawing mode")

            if xp==0 and yp==0:

                xp=x1
                yp=y1 


            if draw_color==(0,0,0):
               #eraser size
               cv2.line(img,(xp,yp),(x1,y1),color=draw_color,thickness=50)
               cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=50)  

            else:
                cv2.line(img,(xp,yp),(x1,y1),color=draw_color,thickness=10) 
                cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_color,thickness=10)    

            xp,yp=x1,y1  

    img_grey=cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)   
    _,img_inv=cv2.threshold(img_grey,20,255,cv2.THRESH_BINARY_INV)      
    img_inv=cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR)


    img=cv2.bitwise_and(img,img_inv)

    img=cv2.bitwise_or(img,img_canvas)

    img=cv2.addWeighted(img,1,img_canvas,0.5,0)         


    cv2.imshow('video',img)
    

    if cv2.waitKey(1) & 0XFF == 27:
        break

cam.release()
cv2.destroyAllWindows()    