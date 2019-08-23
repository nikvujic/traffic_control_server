import socket
import cv2
import numpy as np
from threading import Thread

reference_frame = None
text_font = cv2.FONT_HERSHEY_SIMPLEX

class Server(Thread):

    def run(self):

        while True:
            listensocket = socket.socket()
            Port = 8000
            maxConnections = 10
            IP = socket.gethostname()

            listensocket.bind(('', Port))

            listensocket.listen(maxConnections)

            print("Server started at " + IP + " on port " + str(Port))

            (clientSocket, adress) = listensocket.accept()

            print("New connection made")

            running = True

            while running:
                message = clientSocket.recv(1024).decode()
                print("The moron says:", message)

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
    blur = cv2.medianBlur(difference, 21)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # LANE 1 => SOUTH
    lane1_polygon = np.array([
        [(934, 683), (968, 683), (978, 1076), (944, 1076)]
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

    cv2.putText(frame, f"{lane1_count}", (947, 669), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    # LANE 2 ==> WEST
    lane2_polygon = np.array([
        [(1, 534), (821, 568), (821, 600), (1, 569)]
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

    cv2.putText(frame, f"{lane2_count}", (825, 592), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    # LANE 3 ==> EAST
    lane3_polygon = np.array([
        [(895, 1), (936, 1), (936, 460), (890, 460)]
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

    cv2.putText(frame, f"{lane3_count}", (905, 474), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    lane4_polygon = np.array([
        [(1023, 527), (1850, 533), (1850, 568), (1023, 559)]
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

    cv2.putText(frame, f"{lane4_count}", (1010, 549), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)

    cv2.imshow('display', frame)
    frame = cv2.resize(frame, None, fx=0.65, fy=0.65, interpolation=cv2.INTER_AREA)

    print("Cars on screen:", cars_on_screen)
    while (True):
        if cv2.waitKey(0) == ord('q'):
            break
    cv2.destroyAllWindows()

Server().start()

reference_frame = cv2.imread("reference_frame.png")
reference_frame = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)

image = cv2.imread("screen1.png")

detect_cars(image)