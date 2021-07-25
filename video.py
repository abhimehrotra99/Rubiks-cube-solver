import cv2
import numpy as np
import kociemba
from colors import average_hsv, detect_color
from translation import sol_manual

'''
faces_shown_coords  = [
    [[25,10],[55,10],[85,10],[25,40],[55,40],[85,40],[25,70],[55,70],[85,70]],
    [[125,10],[155,10],[185,10],[125,40],[155,40],[185,40],[125,70],[155,70],[185,70]],
    [[225,10],[255,10],[285,10],[225,40],[255,40],[285,40],[225,70],[255,70],[285,70]],
    [[325,10],[355,10],[385,10],[325,40],[355,40],[385,40],[325,70],[355,70],[385,70]],
    [[425,10],[455,10],[485,10],[425,40],[455,40],[485,40],[425,70],[455,70],[485,70]],
    [[525,10],[555,10],[585,10],[525,40],[555,40],[585,40],[525,70],[555,70],[585,70]]
]
'''

faces = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]
]


blank = np.zeros((480,640,3))

colors = ["white","blue","green","yellow","orange","red","NR"]

positions  = ["Up","Right","Front","Down","Left","Back"]

color_to_position = dict()

colors_bgr_values = {
    "r": (0,0,255),
    "g": (0,255,0),
    "b": (255,0,0),
    "w": (255,255,255),
    "o": (0,85,255),
    "y": (0,217,255),
}


'''
def get_coords(w,h):
    a = 15
    b = 10
    for i in range(6):
        #print(prev_face)
        for j in range(9):
            faces_shown_coords[i][j] = [a+((j%3)*w),b+(int(j/3)*h)]
            print(faces_shown_coords[i][j])
        #print(faces_shown_coords[i][2])
        a = faces_shown_coords[i][2][0]+10
        b = faces_shown_coords[i][2][1]


get_coords(30,30)
'''


cam = cv2.VideoCapture(0)

width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

# MACOS AND LINUX: *'XVID' (MacOS users may want to try VIDX as well just in case)
# WINDOWS *'VIDX'
# writer = cv2.VideoWriter('./rubik_capture.mp4', cv2.VideoWriter_fourcc(*'VIDX'),25, (width, height))


roi_top = int(height/3)
roi_bottom = int(2*height/3)
roi_left = int((width-roi_top)/2)
roi_right = int(roi_left+roi_top)

#chosen for 640*480
w = 25
h = 25
p=[0]*9
p[0] = (130,30)
p[1] = (80,30)
p[2] = (30,30)
p[3] = (130,80)
p[4] = (80,80)
p[5] = (30,80)
p[6] = (130,130)
p[7] = (80,130)
p[8] = (30,130)

confirming_origin = (500,200)

reading = False
calculated = False
confirming = False
curr_face = 0
solution=''
idx = 0
solution_length = 10

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)

    # clone the frame
    frame_copy = frame.copy()

    cv2.putText(frame_copy, 'R', (50,150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))
    cv2.putText(frame_copy, 'L', (580,150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0))
    
    k = cv2.waitKey(1) & 0xFF
    
    if curr_face<6:

        # Grab the ROI from the frame
        roi = frame[roi_top:roi_bottom, roi_left:roi_right]
        hsv_roi = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)

        # Draw ROI Rectangle on frame copy
        cv2.rectangle(frame_copy, (roi_left, roi_top), (roi_right, roi_bottom), (0,0,255), 5)
        cv2.putText(frame_copy, "R - Start/Stop Reading", (400,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))
        cv2.putText(frame_copy, "S - Save Face", (400,80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255))


        if k==ord('r'):
            reading = not reading

        for i in range(9):
            cv2.circle(frame_copy,(roi_left+p[i][0],roi_top+p[i][1]),2,(0,0,0),-1)
            if reading:
                color = detect_color(average_hsv(i, p, hsv_roi))
                if k==ord('s') and not confirming:
                    faces[curr_face][i]=color
            else:
                color = f"{i+1}"
            cv2.putText(frame_copy, color, (roi_left+p[i][0],roi_top+p[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        if reading and k==ord('s'):
            confirming = True
        
        
        if not confirming:
            cv2.putText(frame_copy, f"Read the {positions[curr_face]} layer", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
        else:
            cv2.putText(frame_copy, "Save the face? (y/n)", (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            for i in range(9):
                row = i//3
                col = i%3
                start_x = confirming_origin[0] - col*30
                start_y = confirming_origin[1] + row*30
                cv2.rectangle(frame_copy, (start_x, start_y), (start_x-29, start_y+29), colors_bgr_values[faces[curr_face][i]], -1)
            if k==ord('y'):
                #for i in range(9):
                #cv2.rectangle(blank, (faces_shown_coords[curr_face][i][0], faces_shown_coords[curr_face][i][1]), 
                              #(faces_shown_coords[curr_face][i][0]+30, faces_shown_coords[curr_face][i][1]+30), 
                              #colors_bgr_values[faces[curr_face][i]], -1)
                color_to_position[faces[curr_face][4]] = positions[curr_face]
                curr_face+=1
                confirming = False
            if k==ord('n'):
                confirming = False
              
    elif curr_face==6 and idx<solution_length:
        if(not calculated):
            for i in range(6):
                for j in range(9):
                    solution+=color_to_position[faces[i][j]][0]
            solution = kociemba.solve(solution).split()
            solution_length = len(solution)
            calculated = True
        
        cv2.putText(frame_copy, sol_manual[solution[idx]], (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0))
        cv2.putText(frame_copy, "N - Next", (300,440), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
        
        if k==ord('n'):
            idx+=1
        
        

    # Display the frame with segmented hand
    # writer.write(frame_copy)
    cv2.imshow("Rubik", frame_copy)
    #cv2.imshow("Faces", blank)


    # Close windows with Esc
    if k == 27:
        break

# Release the camera and writer and destroy all the windows
cam.release()
# writer.release()
cv2.destroyAllWindows()

for c in solution:
    print(sol_manual[c])

print(solution)