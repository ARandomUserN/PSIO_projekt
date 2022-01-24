import cv2
import numpy as np


from datetime import datetime

def get_file_name():
    now = datetime.now()
 
    #print("now =", now)

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y%m%d_%H%M%S")
    dt_string = dt_string + '.mp4'
    return dt_string


    
    
device = 0
cap = cv2.VideoCapture('vid_kor.mp4')

frame_limit = 60
    

pos_frame = 0
cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,360)
fps = int(round(cap.get(cv2.CAP_PROP_FPS),0))

dt_string = get_file_name()
output = cv2.VideoWriter(dt_string,cv2.VideoWriter_fourcc(*'MP4V'), 20.0, (640, 360))

first_frame = None
counter = 60
time_ref = datetime.now()

count = 0
f_count = 0
p_count = 0
occ_tmp = 0

prev_percentage = 0

frame_list = []

while not cap.isOpened():
    cap = cv2.VideoCapture('video.webm')
    #cap = cv2.VideoCapture(device)
    cv2.waitKey(2000)
    print("Czekam na wideo")
while True:
    flag, frame = cap.read()
    occuppied = 0
    if flag:
        
        img = np.copy(frame)
        fr = np.copy(frame)
        fr = cv2.resize(fr,(640,360))
        
        frame = cv2.resize(frame, (72, 36))
        
        #print(np.shape(fr),np.shape(frame))
        
        
        pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        gray = cv2.Canny(gray, 50,80)
        
        if first_frame is None:
            first_frame = np.copy(gray)
            output.write(fr)
            f_count = f_count+1
            count = count+1
            
        if(f_count == 20*60): #~1 minute
            print(fps, f_count)
            output.release()
            dt_string = get_file_name()
            
            output = cv2.VideoWriter(dt_string,cv2.VideoWriter_fourcc(*'MP4V'), 24.0, (640, 360))
            output.write(fr)
            f_count=1
            count = 1
            
        count = count+1
        if(f_count > 20*60*10): #~10 minutes
            output.release()
            dt_string = get_file_name()
            
            output = cv2.VideoWriter(dt_string,cv2.VideoWriter_fourcc(*'MP4V'), 24.0, (640, 360))
            output.write(fr)
            count=1
        
        
        delta = cv2.absdiff(first_frame,gray)
        res = delta.astype(np.uint8)
        percentage = (np.count_nonzero(res) * 100)/ res.size
        #print(percentage)
        
        
        if(percentage > 5):
            occuppied = 1
        if(abs(prev_percentage - percentage) < 0.05 and p_count == 0):
            first_frame = np.copy(gray)
            p_count = (frame_limit//2)
            
        p_count = p_count-1
            
        if(count%(frame_limit//2)==0):
            prev_percentage = percentage
        
            
            
            
        frame_list.append(fr)
        if(len(frame_list)> frame_limit):
            frame_list.pop(0)
        if(occuppied):
            for f in range(0,len(frame_list)):
                output.write(frame_list.pop(0))
                f_count = f_count+1
            
            occ_tmp = frame_limit
            
        else:
            if(occ_tmp > 0):
                for f in range(0,len(frame_list)):
                    output.write(frame_list.pop(0))
                    f_count = f_count+1
                    occ_tmp = occ_tmp - 1
                
                    
                
            
            
        cv2.imshow('Frame',cv2.resize(frame,(640,360)))
        cv2.imshow('Gray',cv2.resize(gray,(640,360)))
        cv2.imshow('BG', cv2.resize(first_frame,(640,360)))
        
        occuppied = 0
        
    else:
        
        output.release()
        cap.release()
        cv2.destroyAllWindows()
        break   

        
        #cap = cv2.VideoCapture('testvid.mp4')
        
        #pos_frame = 0
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,360)

    if cv2.waitKey(10) == 27:
        output.release()
        cap.release()
        cv2.destroyAllWindows()
        break   