import socket
import cv2
import numpy as np
from threading import Thread

cap = cv2.VideoCapture("traffic_bird_view.mp4")
reference_frame = None
text_font = cv2.FONT_HERSHEY_SIMPLEX
image_area = None

while True:
    ret, frame = cap.read()

    if ret is False:
        break

    frame = cv2.resize(frame, None, fx=0.5, fy=0.55, interpolation=cv2.INTER_AREA)
    h, w, c = frame.shape

    if reference_frame is None:
        reference_frame = frame
        reference_frame = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)

    image_area = reference_frame.shape[0] * reference_frame.shape[1]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    difference = cv2.absdiff(reference_frame, gray)
    blur = cv2.medianBlur(difference, 51)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    lane1_polygon = np.array([
        [(0, 250), (0, 358), (w, 358), (w, 250)]
    ])
    # cv2.rectangle(frame, (0,250), (w,358), (0,255,0), 3)
    lane1 = np.zeros_like(frame)
    cv2.fillPoly(lane1, lane1_polygon, (255, 255, 255))
    lane1 = cv2.cvtColor(lane1, cv2.COLOR_BGR2GRAY)
    lane1_mask = cv2.bitwise_and(threshold, lane1) 
    
    lane2_polygon = np.array([
        [(0, 400), (0, 488), (w, 488), (w, 400)]
    ])
    # cv2.rectangle(frame, (0,358), (w,488), (255,0,0), 3)
    lane2 = np.zeros_like(frame)
    cv2.fillPoly(lane2, lane2_polygon, (255, 255, 255))
    lane2 = cv2.cvtColor(lane2, cv2.COLOR_BGR2GRAY)
    lane2_mask = cv2.bitwise_and(threshold, lane2) 

    contours1, _ = cv2.findContours(lane1_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(lane2_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)

    contour_count = 0
    for i in contours1:
        if cv2.contourArea(i) > (0.01 * image_area) and contour_area < (0.065 * image_area):
            contour_count += 1
    cv2.putText(frame, f"Cars in lane: {contour_count}", (0, 230), text_font, 0.75, (0,255,0), 2, cv2.LINE_AA)

    contour_count = 0
    for i in contours2:
        if cv2.contourArea(i) > (0.01 * image_area) and contour_area < (0.065 * image_area):
            contour_count += 1
    cv2.putText(frame, f"Cars in lane: {contour_count}", (0, 338), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)
    
    for i in contours1:
        contour_area = cv2.contourArea(i)
        # print("min: ", 0.01 * image_area)
        # print("max: ", 0.065 * image_area)
        # print("contour area1: ", contour_area)
        x, y, w, h = cv2.boundingRect(i)
        if contour_area > (0.01 * image_area) and contour_area < (0.065 * image_area):
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
            cv2.putText(frame, f"{contour_area}", (int((x+w/2)),y-4), text_font, 0.75, (0,255,0), 2, cv2.LINE_AA)
        # else:
        #     cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
        #     cv2.putText(frame, f"{contour_area}", (int((x+w/2)),int(y+(h/2))), text_font, 0.75, (0,0,255), 2, cv2.LINE_AA)

    for i in contours2:
        contour_area = cv2.contourArea(i)
        # print("min: ", 0.01 * image_area)
        # print("max: ", 0.065 * image_area)
        # print("contour area2: ", contour_area)
        x, y, w, h = cv2.boundingRect(i)
        if contour_area > (0.01 * image_area) and contour_area < (0.065 * image_area):
            cv2.rectangle(frame, (x,y-40), (x+w,y+h), (255,0,0), 3)
            cv2.putText(frame, f"{contour_area}", (int((x+w/2)),y-4), text_font, 0.75, (255,0,0), 2, cv2.LINE_AA)
        # else:
        #     cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
        #     cv2.putText(frame, f"{contour_area}", (int((x+w/2)),int(y+(h/2))), text_font, 0.75, (0,0,255), 2, cv2.LINE_AA)

    cv2.imshow('display', frame)

    control = cv2.waitKey(1)
    if control == ord('q'):
        break
    if control == ord(' '):
        if cv2.waitKey(0) == (' '):
            pass
        else:
            pass


cap.release()
cv2.destroyAllWindows()