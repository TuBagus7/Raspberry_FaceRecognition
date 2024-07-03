import cv2
import numpy as np
import face_recognition
import RPi.GPIO as GPIO
import pickle
import threading
import time

# Your GPIO setup goes here
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Load custom encodings
encodingsP = "encodings.pickle"
print("[INFO] loading custom encodings...")
data = pickle.loads(open(encodingsP, "rb").read())


# Function to control solenoids based on GPIO input
def gpio_solenoid_control():
    try:
        GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        while True:
            if GPIO.input(12) == GPIO.HIGH:
                # Solenoid 1
                GPIO.setup(18, GPIO.OUT)
                GPIO.output(18, 1)
                # Solenoid 2
                GPIO.setup(25, GPIO.OUT)
                GPIO.output(25, 0)

                print("Button GPIO12 was pushed. Solenoids are locked!")

            # Add a short delay to avoid excessive checking
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("")


# Improved face recognition loop
def face_recognition_loop():
    cap = cv2.VideoCapture(0)

    try:
        while True:
            try:
                success, img = cap.read()
                
                if not success:  # If reading failed, try to re-initialize the capture
                    print("[INFO] Lost connection to camera, attempting to reconnect...")
                    cap.release()  # Release the current capture object
                    time.sleep(2)  # Wait for a moment before reinitializing
                    cap = cv2.VideoCapture(0)  # Attempt to re-initialize the capture
                    
                    continue  # Skip the rest of the loop and try again
                
                # Proceed with processing if the frame was read successfully
                img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)

                faces_cur_frame = face_recognition.face_locations(img_s)
                encodes_cur_frame = face_recognition.face_encodings(img_s, faces_cur_frame)

                for encode_face, face_loc in zip(encodes_cur_frame, faces_cur_frame):
                    matches = face_recognition.compare_faces(data["encodings"], encode_face)
                    face_dis = face_recognition.face_distance(data["encodings"], encode_face)
                    match_index = np.argmin(face_dis)
                    face_dis_match_index = face_dis[match_index]
                    percentage_match = round((1 - face_dis_match_index) * 100, 2)
                    name = "Unknown"

                    if matches[match_index]:
                        if face_dis_match_index < 0.4 and percentage_match >= 60:
                            name = data["names"][match_index].upper()
                            
                            # Solenoid control based on recognized face
                            if name == "WAHYU":
                                GPIO.setup(18, GPIO.OUT)
                                GPIO.output(18, 0)  # Turn on solenoid1
                                print(f"Recognized: {name}. Turning on solenoid1")
                            elif name == "ALDI":
                                GPIO.setup(25, GPIO.OUT)
                                GPIO.output(25, 1)  # Turn on solenoid2
                                print(f"Recognized: {name}. Turning on solenoid2")
                        
                    print(name)
                    results = f"{name} {percentage_match}%"

                    y1, x2, y2, x1 = face_loc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, results, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                cv2.imshow("Webcam", img)
                key = cv2.waitKey(1) & 0xFF

                # quit when 'q' or 'esc' key is pressed
                if key == ord("q") or key == 27:
                    break
            
            except Exception as e:
                print(f"[ERROR] An error occurred: {e}")
                
                break  # Exit the loop in case of an error
    except KeyboardInterrupt:
        print("")
    finally:
        cv2.destroyAllWindows()
        cap.release()


# Run both threads concurrently
try:
    # Create threads
    recognition_thread = threading.Thread(target=face_recognition_loop)
    gpio_thread = threading.Thread(target=gpio_solenoid_control)

    # Start threads
    recognition_thread.start()
    gpio_thread.start()

    # Wait for threads to finish
    recognition_thread.join()
    gpio_thread.join()
except KeyboardInterrupt:
    print("Keyboard Interrupt. Exiting...")
finally:
    GPIO.cleanup()
