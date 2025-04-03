import argparse
import imutils
import cv2
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image containing ArUco tag(s)")
ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUco tag to detect")
args = vars(ap.parse_args())

#dictionary of accepted marker types. add to this if really necessary
ARUCO_DICT = {"DICT_6X6_250": cv2.aruco.DICT_6X6_250}


#load input images and resize
print("loading image...")
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)

#verify that the supplied ArUco tag exists and is supported by OpenCV
if ARUCO_DICT.get(args["type"], None) is None:
	print("ArUco tag of '{}' is not supported".format(args["type"]))
	sys.exit(0)

#load the ArUco disctionary, grab the ArUco params, and detect markers
print("detecting '{}' tags...".format(args["type"]))
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[args["type"]])
arucoParams = cv2.aruco.DetectorParameters()
(corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict, parameters = arucoParams)

#verify detection
if len(corners) > 0:
	ids = ids.flatten()
	
	
	#loop over detected ArUco marker corners
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
		cv2.line(image, topLeft, topRight, green, 2)
		cv2.line(image, topRight, bottomRight, green, 2)
		cv2.line(image, bottomRight, bottomLeft, green, 2)
		cv2.line(image, bottomLeft, topLeft, green, 2)
		
		#compute the marker center (distance formula)
		cX = int((topLeft[0] + bottomRight[0]) / 2.0)
		cY = int((topLeft[1] + bottomRight[1]) / 2.0)
		cv2.circle(image, (cX,cY), 4, blue, -1)
		
		#draw the marker's ID on the image
		cv2.putText(image, str(markerID), (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, green, 2)
		print("ArUco Marker ID: {}".format(markerID))
		
	#show the output
	cv2.imshow("Image", image)
	cv2.waitKey(0)
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

