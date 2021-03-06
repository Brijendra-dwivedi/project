# USAGE
# python blur_detector_image.py --image images/resume_01.png --thresh 27

# import the necessary packages
from blur_detector import detect_blur_fft
import numpy as np
import imutils
import cv2

# construct the argument parser and parse the arguments

# load the input image from disk, resize it, and convert it to
# grayscale
def detect_image_blur(path,threshold=20,visualize=-1,test=-1):
	orig = cv2.imread(path)
	orig = imutils.resize(orig, width=500)
	gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)

	# apply our blur detector using the FFT
	(mean, blurry) = detect_blur_fft(gray, size=60,thresh=threshold, vis=visualize > 0)

	# draw on the image, indicating whether or not it is blurry
	image = np.dstack([gray] * 3)
	color = (0, 0, 255) if blurry else (0, 255, 0)
	text = "Blurry ({:.4f})" if blurry else "Not Blurry ({:.4f})"
	text = text.format(mean)
	cv2.putText(image, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
		color, 2)
	print("[INFO] {}".format(text))

	# show the output image
	#cv2.imshow("Output", image)
	#cv2.waitKey(0)

	# check to see if are going to test our FFT blurriness detector using
	# various sizes of a Gaussian kernel
	if test > 0:
		image_array=[]
		# loop over various blur radii
		for radius in range(1, 30, 2):
			# clone the original grayscale image
			image = gray.copy()

			#check to see if the kernel radius is greater than zero
			if radius > 0:
				# blur the input image by the supplied radius using a
				# Gaussian kernel
				image = cv2.GaussianBlur(image, (radius, radius), 0)

				# apply our blur detector using the FFT
				(mean, blurry) = detect_blur_fft(image, size=60,thresh=threshold, vis=visualize > 0)

				# draw on the image, indicating whether or not it is
				# blurry
				image = np.dstack([image] * 3)
				color = (0, 0, 255) if blurry else (0, 255, 0)
				text = "Blurry ({:.4f})" if blurry else "Not Blurry ({:.4f})"
				text = text.format(mean)
				cv2.putText(image, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
					0.7, color, 2)
				print("[INFO] Kernel: {}, Result: {}".format(radius, text))

			# show the image
			#cv2.imshow("Test Image", image)
			#cv2.waitKey(0)
			image_array.append(image)
		return image_array
	return image, mean, blurry