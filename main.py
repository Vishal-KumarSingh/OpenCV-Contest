import cv2
import random
car_classifier = cv2.CascadeClassifier('input/haarsascade.xml')
videoStream = cv2.VideoCapture("input/DRONE-SURVEILLANCE-CONTEST-VIDEO.mp4")
width = 540
node_change_rate = 19/3
droneSpeed = float(540) / node_change_rate
#print(droneSpeed)
vw = cv2.VideoWriter("output/output.avi" , cv2.VideoWriter_fourcc('M','J','P','G') , 10 ,(960,540) )
def searching(element , sensitivness , arr):
    count = 0
    for item in arr:
        count +=1
        if (element > item-sensitivness) and (element<item + sensitivness):
            #print("element found")
            #print(count)
            return count
    #print("element not found")
    return -1

def namePrinter(img):
    cv2.putText(img , "VISHAL KUMAR SINGH", (405,50), cv2.FONT_HERSHEY_TRIPLEX, 0.7 , (0,0,255), cv2.LINE_4 )
def carPrinter(img , no):
    cv2.putText(img , str(no), (850,50), cv2.FONT_HERSHEY_TRIPLEX, 0.7 , (0,0,255), cv2.LINE_4 )
no_of_cars = 0
prev_cars_y = []
prev_cars_x = []
try:
    while True:
        suc,img = videoStream.read()
        # length - 21 /9 -> 2.33
        #imgGray.resize((100,200))
        #cv2.imshow("GRay",imgGray)
        small = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
        print(small.shape)
        imgGray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        cars = car_classifier.detectMultiScale(imgGray, 1.1, 2)

        for (x, y, w, h) in cars:
            index = searching(y, 45, prev_cars_y)
            color = (0,0,255)
            if searching(x , 20 , prev_cars_x)==-1:

                if index==-1:
                    no_of_cars += 1

            #print("index = "+ str(index))
            cv2.putText(small, str(index), (x, y + h), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 0, 255), cv2.LINE_4)
            cv2.rectangle(small, (x, y), (x + w, y + h), color, 2)

        prev_cars_y = []
        prev_cars_x = []
        for (x, y, w, h) in cars:
            prev_cars_y.append(y)
            prev_cars_x.append(x)
        prev_cars_y.sort()
        prev_cars_x.sort()
        #print(prev_cars_y)
        namePrinter(small)
        carPrinter(small , no_of_cars)
        cv2.imshow("Out" , small)
        vw.write(small)
        cv2.waitKey(1)
except Exception:
    pass
vw.release()