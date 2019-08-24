import socket
import cv2
import numpy as np
import os
import io
import os.path
import time
from threading import Thread

reference_frame = None
text_font = cv2.FONT_HERSHEY_SIMPLEX

class FrameReceiver(Thread):

    def run(self):

        while True:
            listensocket = socket.socket()
            Port = 8000
            maxConnections = 5
            IP = socket.gethostname()

            listensocket.bind(('', Port))
            listensocket.listen(maxConnections)

            print("Server started at " + IP + " on port " + str(Port))

            (clientSocket, adress) = listensocket.accept()

            print("New connection made")
            
            if os.path.isfile("traffic_data.png"):
                os.remove("traffic_data.png")
                
            file = open("traffic_data.png", "w+b")
            
            start = time.time()

            while True:
                data = clientSocket.recv(1024)
            
                if not data:
                    file.write(data)
                    break
            
                file.write(data)

            end = time.time()

            print("Image transfer time:", round(end - start, 2))
            print("Done.")


class TrafficLigth(Thread):

    def run(self):
        listensocket = socket.socket()
        Port = 8001
        maxConnections = 5
        IP = socket.gethostname()

        listensocket.bind(('', Port))
        listensocket.listen(maxConnections)

        print("Server started at " + IP + " on port " + str(Port))

        (clientSocket, adress) = listensocket.accept()

        print("New connection made")

        while (True):
            try:
                clientSocket.send(b"1")
                print("start sent")
                time.sleep(12)
                clientSocket.send(b"0")
                print("stop sent")
                time.sleep(12)
            except:
                print("Connection closed")
                break          

def detect_cars(frame):
    cars_on_screen = 0
    lane1_count = 0
    lane2_count = 0
    lane3_count = 0
    lane4_count = 0

    h, w, c = frame.shape

    if (reference_frame is None):
        print("No reference frame")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    difference = cv2.absdiff(reference_frame, gray)
    blur = cv2.medianBlur(difference, 11)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # LANE 1 => SOUTH
    lane1_polygon = np.array([
        [(934, 662), (968, 662), (978, 1078), (944, 1078)]
    ])
    # cv2.polylines(frame,[lane1_polygon],True,(0,255,0), 2)
    lane1 = np.zeros_like(frame)
    cv2.fillPoly(lane1, lane1_polygon, (255, 255, 255))
    lane1 = cv2.cvtColor(lane1, cv2.COLOR_BGR2GRAY)
    lane1_mask = cv2.bitwise_and(threshold, lane1)

    contours1, _ = cv2.findContours(lane1_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in contours1:
        contour_area = cv2.contourArea(i)
        x, y, w, h = cv2.boundingRect(i)
        if (contour_area > 10):  
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 3)
            cars_on_screen += 1
            lane1_count += 1

    cv2.putText(frame, f"{lane1_count}", (947, 649), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    # LANE 2 ==> WEST
    lane2_polygon = np.array([
        [(1, 507), (487, 532), (804, 540), (804, 570), (469, 567), (1, 544)]
    ])
    # cv2.polylines(frame,[lane2_polygon],True,(0,255,0), 2)
    lane2 = np.zeros_like(frame)
    cv2.fillPoly(lane2, lane2_polygon, (255, 255, 255))
    lane2 = cv2.cvtColor(lane2, cv2.COLOR_BGR2GRAY)
    lane2_mask = cv2.bitwise_and(threshold, lane2)

    contours2, _ = cv2.findContours(lane2_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in contours2:
        contour_area = cv2.contourArea(i)
        x, y, w, h = cv2.boundingRect(i)
        if (contour_area > 10):
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
            cars_on_screen += 1
            lane2_count += 1

    cv2.putText(frame, f"{lane2_count}", (825, 566), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    # LANE 3 ==> EAST
    lane3_polygon = np.array([
        [(895, 1), (928, 1), (928, 411), (890, 411)]
    ])
    # cv2.polylines(frame,[lane3_polygon],True,(0,255,0), 2)
    lane3 = np.zeros_like(frame)
    cv2.fillPoly(lane3, lane3_polygon, (255, 255, 255))
    lane3 = cv2.cvtColor(lane3, cv2.COLOR_BGR2GRAY)
    lane3_mask = cv2.bitwise_and(threshold, lane3)

    contours3, _ = cv2.findContours(lane3_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in contours3:
        contour_area = cv2.contourArea(i)
        x, y, w, h = cv2.boundingRect(i)
        if (contour_area > 10):
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 3)
            cars_on_screen += 1
            lane3_count += 1

    cv2.putText(frame, f"{lane3_count}", (905, 440), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    lane4_polygon = np.array([
        [(1053, 495), (1830, 510), (1830, 539), (1054, 529)]
    ])
    # cv2.polylines(frame,[lane4_polygon],True,(0,255,0), 2)
    lane4 = np.zeros_like(frame)
    cv2.fillPoly(lane4, lane4_polygon, (255, 255, 255))
    lane4 = cv2.cvtColor(lane4, cv2.COLOR_BGR2GRAY)
    lane4_mask = cv2.bitwise_and(threshold, lane4)

    contours4, _ = cv2.findContours(lane4_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in contours4:
        contour_area = cv2.contourArea(i)
        x, y, w, h = cv2.boundingRect(i)
        if (contour_area > 10):
            cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,255), 3)
            cars_on_screen += 1
            lane4_count += 1

    cv2.putText(frame, f"{lane4_count}", (1010, 524), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    frame = cv2.resize(frame, None, fx=0.65, fy=0.65, interpolation=cv2.INTER_AREA)
    cv2.imshow('display', frame)

    print("Cars on screen:", cars_on_screen)
    while (True):
        if cv2.waitKey(0) == ord('q'):
            break
    cv2.destroyAllWindows()

# FrameReceiver().start()    
TrafficLigth().start()

reference_frame = cv2.imread("reference_frame.png")
reference_frame = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)

image = cv2.imread("traffic_data.jpg")

if (image is not None):
    detect_cars(image)