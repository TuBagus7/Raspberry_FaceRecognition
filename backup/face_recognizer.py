# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import RPi.GPIO as GPIO

# Initialize 'currentname' to trigger only when a new person is identified.
currentname = "unknown"
# Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
vs = VideoStream(src=0, framerate=10).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# start the FPS counter
fps = FPS().start()

# If code is stopped while the solenoid is active it stays active
# This may produce a warning if the code is restarted and it finds the GPIO Pin, which it defines as non-active in next line, is still active
# from previous time the code was run. This line prevents that warning syntax popping up which if it did would stop the code running.
GPIO.setwarnings(False)
# This means we will refer to the GPIO pins
# by the number directly after the word GPIO. A good Pin Out Resource can be found here https://pinout.xyz/
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

# loop over frames from the video file stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)
    # Detect the fce boxes
    boxes = face_recognition.face_locations(frame)
    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"  # if face is not recognized, then print Unknown

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)

            # If someone in your dataset is identified, print their name on the screen
            if currentname != name:
                currentname = name
                print(currentname)

                if currentname == "Wahyu":
                    # Turns Relay On for channel pin 18 and unlock the door solenoid if the face is identified and matched.
                    # Brings Voltage to Min GPIO can output ~0V.
		    # GPIO.setup(18, GPIO.OUT)
                    GPIO.output(18, 0)
                elif currentname == "Tama":
                    # Turns Relay On for channel pin 25 and unlock the door solenoid if the face is identified and matched.
                    # Brings Voltage to Min GPIO can output ~0V.
		    # GPIO.setup(25, GPIO.OUT)
                    GPIO.output(25, 1)
        # else:
        #     # This Turns Relay Off for both channel pin and lock the door solenoid if the face is unknown.
        #     # Brings Voltage to Max GPIO can output ~3.3V
        #     GPIO.output(chan_list, 1)

        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    .8, (0, 255, 255), 2)

    # display the image to our screen
    # Comment imshow, because we want to running this script in background process
    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    # quit when 'q' key is pressed
    if key == ord("q"):
        break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
