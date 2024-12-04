import cv2
import imutils
import numpy as np
import serial  # For serial communication

# global variables
bg = None

# Serial setup (set the correct port and baud rate)
ser = serial.Serial('COM10', 9600)  # Replace 'COM3' with your port

def run_avg(image, aWeight):
    global bg
    if bg is None:
        bg = image.copy().astype("float")
        return
    cv2.accumulateWeighted(image, bg, aWeight)

def segment(image, threshold=25):
    global bg
    diff = cv2.absdiff(bg.astype("uint8"), image)
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return
    else:
        segmented = max(contours, key=cv2.contourArea)
        return (thresholded, segmented)

def count_fingers(thresholded, segmented):
    hull = cv2.convexHull(segmented, returnPoints=False)
    defects = cv2.convexityDefects(segmented, hull)
    if defects is None:
        return 0
    
    count = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(segmented[s][0])
        end = tuple(segmented[e][0])
        far = tuple(segmented[f][0])
        a = np.linalg.norm(np.array(start) - np.array(end))
        b = np.linalg.norm(np.array(start) - np.array(far))
        c = np.linalg.norm(np.array(end) - np.array(far))
        angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
        
        if angle <= np.pi / 2 and d > 10000:
            count += 1
    return count

def main():
    aWeight = 0.5
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    top, right, bottom, left = 10, 350, 225, 590
    num_frames = 0
    start_recording = False

    while True:
        (grabbed, frame) = camera.read()
        if not grabbed:
            print("[Warning!] Error input, Please check your camera or video.")
            break
        
        frame = imutils.resize(frame, width=700)
        frame = cv2.flip(frame, 1)
        clone = frame.copy()
        (height, width) = frame.shape[:2]
        roi = frame[top:bottom, right:left]
        
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 30:
            run_avg(gray, aWeight)
            print(num_frames)
        else:
            hand = segment(gray)
            if hand is not None:
                (thresholded, segmented) = hand
                finger_count = count_fingers(thresholded, segmented)
                
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                cv2.imshow("Thresholded", thresholded)

                # Send the finger count over serial
                ser.write(f"{finger_count}\n".encode())
                print(f"Finger count: {finger_count}")
            
            cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)
        num_frames += 1
        cv2.imshow("Video Feed", clone)
        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord("q"):
            break

    camera.release()
    ser.close()
    cv2.destroyAllWindows()

main()
