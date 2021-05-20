# USAGE
# python blur_detector_video.py

# import the necessary packages
from os import path

from blur_detector import detect_blur_fft
import argparse
import imutils
import time
import cv2



# initialize the video stream and allow the camera sensor to warm up
def detect_video_blur(path, threshold=20):
	print("[INFO] starting video ...")
	vs = cv2.VideoCapture(path)
	time.sleep(2.0)

	# loop over the frames from the video stream
	while True:
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 400 pixels
		_,frame = vs.read()
		frame = imutils.resize(frame, width=500)

		# convert the frame to grayscale and detect blur in it
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		(mean, blurry) = detect_blur_fft(gray, size=60,thresh=threshold, vis=False)

		# draw on the frame, indicating whether or not it is blurry
		color = (0, 0, 255) if blurry else (0, 255, 0)
		text = "Blurry ({:.4f})" if blurry else "Not Blurry ({:.4f})"
		text = text.format(mean)
		cv2.putText(frame, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
			0.7, color, 2)

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1)

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()