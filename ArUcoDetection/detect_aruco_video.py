from imutils.video import VideoStream
from picamera2 import Picamera2
import argparse
import imutils
import time
import cv2
import sys


#create arguments for command line
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUco tag to detect")
args = vars(ap.parse_args())

#dictionary of accepted marker types. add to this if really necessary
ARUCO_DICT = {"DICT_6X6_250": cv2.aruco.DICT_6X6_250}

#verify that the supplied ArUco tag exists and is supported by OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
	print("ArUco tag of '{}' is not supported".format(args["type"]))
	sys.exit(0)
	
#load the ArUco disctionary, grab the ArUco params, and detect markers
print("detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters()

#initialize video stream
camera = Picamera2()
camera.resolution = (640,480)
camera.framerate = 32
camera.start()

#loop over streamed frames
while True:
	array = camera.capture_array()
	array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
	(corners, ids, rejected) = cv2.aruco.detectMarkers(array, arucoDict, parameters = arucoParams)
	if len(corners) > 0:
		ids = ids.flatten()
		
		for (markerCorner, markerID) in zip(corners, ids):
			#extract. order: top-left, top-right, bottom-right, bottom-left
			corners = markerCorner.reshape((4,2))
			(topLeft, topRight, bottomRight, bottomLeft) = corners
		
			#convert each (x,y) pair into ints
			topRight = (int(topRight[0]), int(topRight[1]))
			topLeft = (int(topLeft[0]), int(topLeft[1]))
			bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
			bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
		
			#draw the lines
			green = (0, 255, 0)
			blue = (0,0,255)
			cv2.line(array, topLeft, topRight, green, 2)
			cv2.line(array, topRight, bottomRight, green, 2)
			cv2.line(array, bottomRight, bottomLeft, green, 2)
			cv2.line(array, bottomLeft, topLeft, green, 2)
		
			#compute the marker center (distance formula)
			cX = int((topLeft[0] + bottomRight[0]) / 2.0)
			cY = int((topLeft[1] + bottomRight[1]) / 2.0)
			cv2.circle(array, (cX,cY), 4, blue, -1)

			#draw the marker's ID on the image
			cv2.putText(array, str(markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, green, 2)
			
	cv2.imshow("Frame", array)
	key = cv2.waitKey(1) & 0xFF
	
	if key == ord("q"):
		break
		
		
cv2.destroyAllWindows()

