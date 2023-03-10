import cv2
import numpy as np
import math
import os
import time
import random
import json

calibration = np.load("/Users/chaitalibhattacharyya/Desktop/ARE/calib_data_AVER/MultiMatrix.npz")

mtx= calibration["camMatrix"]
dist = calibration["distCoef"]

marker1_id = 101
marker2_id = 100
marker3_id = 102

cap = cv2.VideoCapture(1)


# data_list = []
# filename = "dataset2.txt"
# if os.path.exists(filename):
#     # If it exists, load the data from the file
#     with open(filename, "r") as f:
#         lines = f.readlines()
#         for line in lines:
#             data = line.strip().split("\t")
#             distance = float(data[0])
#             data_list.append([distance,0])
#     # Remove the file to avoid appending the same data multiple times
#     os.remove(filename)
    
data_list = []
if os.path.exists("dataset3.txt"):
    # If it exists, load the data from the file
    with open("dataset3.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            data = line.strip().split("\t")
            distance1 = float(data[0])
            distance2 = float(data[1])
            angle = float(data[2])
            data_list.append([distance1,distance2,angle])
    # Remove the file to avoid appending the same data multiple times
    os.remove("dataset3.txt")




while True:
    ret, frame = cap.read()
    
    if frame is None:
        # Restart the loop to check for the next latest added video file
        break
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000))
    # 마커 2개 보일때   
    if ids is None:
        print("마커 없습니다")
    elif ids is not None and len(ids) == 2:
        marker1_index = None
        marker2_index = None
        for i in range(len(ids)):
            if ids[i] == marker1_id:
                marker1_index = i
            elif ids[i] == marker2_id:
                marker2_index = i
            elif ids[i] == marker3_id:
                marker2_index = i
                
        if marker1_index is not None and marker2_index is not None:
            #마커 정보 r 과 t
            rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker1_index], 17.0, mtx, dist)
            rvec2, tvec2, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker2_index], 17.0, mtx, dist)
            distance = cv2.norm(tvec1-tvec2)
            print("2개 마커 사이의 거리:", distance)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            data_list.append([distance,0])
            filename1 = "dataset2_" + str(int(time.time())) +  "_" + str(random.randint(1, 10000)) + ".txt"  # add a timestamp to the filename
            with open("dataset2.txt", "a") as f:
                for data in data_list:
                    f.write("{:.2f}\t{:.2f}\n".format(data[0], data[1]))
                data_list.clear()
            with open("dataset2.txt") as f:
                lines = f.readlines()
            max_cols = 0
            for line in lines:
                row = line.strip().split() 
                max_cols = max(max_cols, len(row))
                if max_cols == 2:
                    col1_sum1 = 0  
                    col2_sum1 = 0  
                    for line in lines:
                        cols1 = line.split()
                        col1_sum1 += float(cols1[0])
                        col2_sum1 += float(cols1[1])
                        num_rows1 = len(lines)
                    col1_avg1 = col1_sum1 / num_rows1
                    col2_avg1 = col2_sum1 / num_rows1

                    print("Average of column 1:", col1_avg1)
                    print("Average of column 2:", col2_avg1)

                    # Define the JSON data
                    data_마커_2개 = {
                        "result": [
                            {"distance1": col1_avg1},
                        ]
                    }

                    # Save the data to a file
                    with open('data_마커_2개.json', 'w') as f:
                        json.dump(data_마커_2개, f)
            point1 = cv2.drawFrameAxes(frame, mtx, dist, rvec1, tvec1 ,  4,9)
            point2 = cv2.drawFrameAxes(frame, mtx, dist, rvec2, tvec2 ,  4,9)
            frame_markers = cv2.aruco.drawDetectedMarkers(frame,corners,ids,(0,255,0))
            
            for i in range(len(ids)):
            
                id_num = str(ids[i][0])
                
                
                center = tuple(map(int, corners[i][0].mean(axis=0)))
                
                
                cv2.putText(frame_markers, id_num, center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            
                cv2.imshow("Frame", frame_markers)

            

    if ids is not None and len(ids) >= 3:
        marker1_index = None
        marker2_index = None
        marker3_index = None
        for i in range(len(ids)):
            if ids[i] == marker1_id:
                marker1_index = i
            elif ids[i] == marker2_id:
                marker2_index = i
            elif ids[i] == marker3_id:
                marker3_index = i
                
        if marker1_index is not None and marker2_index is not None and marker3_index is not None:
            #마커 정보 r 과 t
            rvec1, tvec1, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker1_index], 17.0, mtx, dist)
            rvec2, tvec2, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker2_index], 17.0, mtx, dist)
            rvec3, tvec3, _ = cv2.aruco.estimatePoseSingleMarkers(corners[marker3_index], 17.0, mtx, dist)
    
            # 거리 계산
            
            distance1 = cv2.norm(tvec1-tvec2)
            distance2 = cv2.norm(tvec1-tvec3)
            distance3 = cv2.norm(tvec2 - tvec3)
            angle = np.cos((distance1**2+distance3**2-distance2**2)/2*distance1*distance3)

            data_list.append([distance1,distance2,angle])
            filename1 = "dataset3_" + str(int(time.time())) +  "_" + str(random.randint(1, 10000)) + ".txt"  # add a timestamp to the filename
            with open("dataset3.txt", "a") as f:
                for data in data_list:
                    f.write("{:.2f}\t{:.2f}\t{:.2f}\n".format(data[0], data[1], data[2]))
                data_list.clear()
            with open("dataset3.txt") as f:
                lines = f.readlines()
            max_cols = 0
            for line in lines:
                row = line.strip().split()
                max_cols = max(max_cols, len(row))
                col1_sum = 0
                col2_sum = 0
                col3_sum = 0
                num_rows = len(lines)

                for line in lines:
                    cols = line.split()
                    col1_sum += float(cols[0])
                    col2_sum += float(cols[1])
                    col3_sum += float(cols[2])

                col1_avg = col1_sum / num_rows
                col2_avg = col2_sum / num_rows
                col3_avg = col3_sum / num_rows

                print("Average of column 1:", col1_avg)
                print("Average of column 2:", col2_avg)
                print("Average of column 3:", col3_avg)


                # Define the JSON data
                data_마커_3개 = {
                    "result": [
                        {"distance1": col1_avg,
                        "distance2": col2_avg,
                        "angle": col3_avg}
                    ]
                }

                # Save the data to a file
                with open('data_마커_3개.json', 'w') as f:
                    json.dump(data_마커_3개, f)
                    
            print("마커 1 과 마커 2 사이의 거리:", distance1)
            print("마커 1 과 마커 3 사이의 거리:", distance2)
            print("마커 2 과 마커 3 사이의 거리:", distance3)
            
            # point1 = cv2.drawFrameAxes(frame, mtx, dist, rvec1, tvec1 ,  9,4)
            # point2 = cv2.drawFrameAxes(frame, mtx, dist, rvec2, tvec2 ,  9,4)
            # point3 = cv2.drawFrameAxes(frame, mtx, dist, rvec3, tvec3 , 9,4)
            
            # frame_markers = cv2.aruco.drawDetectedMarkers(frame,corners,ids,(0,255,0))
            # for i in range(len(ids)):
            
            #     id_num = str(ids[i][0])
                
                
            #     center = tuple(map(int, corners[i][0].mean(axis=0)))
                
            #     # Draw the ID number on the frame at the center of the marker
            #     # cv2.putText(frame_markers, id_num, center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, "Distance between marker 1 and marker 2: {:.2f}".format(round(distance1,2)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
            cv2.putText(frame, "Distance between marker 1 and marker 3: {:.2f}".format(round(distance2,2)), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    



            
        
cap.release()
cv2.destroyAllWindows()

            
