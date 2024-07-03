# This script isn't quite workable
# import cv2
# import os

# cam = cv2.VideoCapture(0)
# cam.set(3, 640)  # set video width
# cam.set(4, 480)  # set video height

# face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# # For each person, enter one numeric face id
# face_id = input('\n enter user id end press <return> ==>  ')
# print("\n [INFO] Initializing face capture. Look the camera and wait ...")

# # Initialize individual sampling face count
# count = 0
# while (True):
#     ret, img = cam.read()
#     cv2.imshow('image', img)
#     img = cv2.flip(img, -1)  # flip video image vertically
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = face_detector.detectMultiScale(gray, 1.3, 5)

#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
#         count += 1
#         # Save the captured image into the datasets folder
#         cv2.imwrite("dataset/User." + str(face_id) + '.' +
#                     str(count) + ".jpg", gray[y:y+h, x:x+w])
#         # cv2.imshow('image', img)

#     k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
#     if k == 27:
#         break
#     elif count >= 30:  # Take 30 face sample and stop video
#         break

# # Do a bit of cleanup
# print("\n [INFO] Exiting Program and cleanup stuff")
# cam.release()
# cv2.destroyAllWindows()


# So, I try this one instead
import cv2

name = 'rinaldi'  # replace with your name

cam = cv2.VideoCapture(0)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 640, 480)

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name = "dataset/" + name + "/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
