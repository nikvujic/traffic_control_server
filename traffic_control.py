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
lane1_count = 0
lane2_count = 0
lane3_count = 0
lane4_count = 0


class FrameReceiver(Thread):

    def run(self):

        while True:
            listensocket = socket.socket()
            port = 8000
            maxConnections = 5
            IP = "0.0.0.0"

            listensocket.bind(('', port))
            listensocket.listen(maxConnections)

            print("Frame transfer server started at " + IP + " on port " + str(port))
            img_count = 0
            while True:
                (clientSocket, adress) = listensocket.accept()

                print("Picture transfer started", adress)

                file = open(f"traffic_data{img_count}.jpg", "w+b")

                start = time.time()

                while True:
                    data = clientSocket.recv(1024)

                    if not data:
                        break

                    qfile.write(data)

                end = time.time()
                print(
                    f"Image transfer time: {round(end - start, 2)} THREAD SIGNAL HERE")

                detect_cars(f"traffic_data{img_count}.jpg")
                
                img_count += 1


class TrafficLigth(Thread):

    def run(self):
        listensocket = socket.socket()
        Port = 8001
        maxConnections = 5
        IP = socket.gethostname()

        listensocket.bind(('', Port))
        listensocket.listen(maxConnections)

        print("Traffic control server started at " + IP + " on port " + str(Port))

        (clientSocket, adress) = listensocket.accept()

        print("New connection made")

        while (True):
            try:
                clientSocket.send(b"1")
                time.sleep(12)
                clientSocket.send(b"0")
                time.sleep(12)
            except:
                print("Connection closed")
                break          

def detect_cars(path_to_frame):
    global lane1_count
    global lane2_count
    global lane3_count
    global lane4_count

    lane1_count = 0
    lane2_count = 0
    lane3_count = 0
    lane4_count = 0
    cars_on_screen = 0

    frame = cv2.imread(path_to_frame)

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
        [(944, 682), (968, 682), (973, 1058), (949, 1058)]
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

    cv2.putText(frame, f"{lane1_count}", (973, 677), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    # LANE 2 ==> WEST
    lane2_polygon = np.array([
        [(315, 577), (487, 586), (860, 600), (860, 620), (500, 612), (315, 600)]
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

    cv2.putText(frame, f"{lane2_count}", (868, 642), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    # LANE 3 ==> EAST
    lane3_polygon = np.array([
        [(921, 16), (943, 16), (938, 519), (914, 519)]
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

    cv2.putText(frame, f"{lane3_count}", (892, 525), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    lane4_polygon = np.array([
        [(1021, 570), (1515, 575), (1515, 601), (1021, 595)]
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

    cv2.putText(frame, f"{lane4_count}", (1022, 564), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    frame = cv2.resize(frame, None, fx=0.65, fy=0.65, interpolation=cv2.INTER_AREA)
    cv2.imshow('display', frame)

    print("Cars on screen:", cars_on_screen)

    print("LANE_COUNT:")
    print(f"  {lane3_count}")
    print(f"{lane2_count}   {lane4_count}")
    print(f"  {lane1_count}")

    # cv2.waitKey(0)
    cv2.destroyAllWindows()

# start the threads
FrameReceiver().start()    
TrafficLigth().start()

# set up reference frame
reference_frame = cv2.imread("reference_frame.jpg")
reference_frame = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)

# clean up frames from last session
for i in range(0, 1000):
    if os.path.exists(f"traffic_data{i}.jpg"):
        os.remove(f"traffic_data{i}.jpg")
    else:
        break