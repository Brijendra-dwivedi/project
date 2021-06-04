# USAGE
# python blur_detector_video.py

# import the necessary packages
from os import path

from blur_detector import detect_blur_fft
import argparse
import imutils
import time
import cv2
from converter import convert_video

# initialize the video stream and allow the camera sensor to warm up
def detect_video_blur(path,output,size=60, threshold=20,vis=False):
	vs = cv2.VideoCapture(path)
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(vs.get(3)), int(vs.get(4))),True)
	blurry_vid= cv2.VideoWriter('output_blur.avi', fourcc, 20.0, (int(vs.get(3)), int(vs.get(4))),True)
	# loop over the frames from the video stream
	frame_removed = 0
	frame_kept = 0
	total_frames = 0
	print("[>>>] starting processing ...")
	while True:
		state,frame = vs.read()
		if state:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			(mean, blurry) = detect_blur_fft(gray, size=size, thresh=threshold, vis=vis)
			if not blurry:
				frame_kept += 1
				out.write(frame)
				print('.',end='')
			else:
				frame_removed+=1
				blurry_vid.write(frame)
			total_frames += 1
			if cv2.waitKey(1) == 27:
				break
		else :
			print('video frame read')
			break
		

	# do a bit of cleanup
	
	vs.release()
	out.release()
	blurry_vid.release()
	cv2.destroyAllWindows()
	print("total frame =>",total_frames)
	print("frame removed =>",frame_removed)
	print("frame kept =>",frame_kept)
	result = convert_video('output.avi')
	return 'output.avi',result

if __name__ =="__main__":
	detect_video_blur(r"videos\OpenCV 3 Python blur detection.mp4","blurv.mp4")
# folder open kro
