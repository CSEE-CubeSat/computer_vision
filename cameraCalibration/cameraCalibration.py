import numpy as np 
import cv2 as cv
import glob

################## FIND CHESSBOARD CORNERS - OBJECT POINTS AND IMAGE POINTS ################## 

CHECKERBOARD = (9,6)
frameSize = (640,480)
# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0) 
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = []# 3D points in real world space
imgpoints = []# 2D points in image plane

images = glob.glob('*.jpg')

for image in images:
	img = cv.imread(image)
	gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	
	# Find the chessboard corners
	ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, None) 
	
	# If found, add object points, image points (after refining them)
	if ret == True:
		
		objpoints.append(objp)
		corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
		imgpoints.append(corners)
		
		#Draw and display the corners
		cv.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
		cv.imshow('img', img)
		cv.waitKey(0)
		
cv.destroyAllWindows()


################## CALIBRATION ################################################################ 

ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

################## UNDISTORTION ###############################################################

img = cv.imread('file.jpg')
h, w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

# Undistort
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

# Crop the image
x, y, w, h = roi
dst = dst[y:t+h , x:x+w]
cv.imwrite('fileResult1.jpg', dst)

# Undistort with Remapping
mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

# Crop the image
x, y, w, h = roi
dst = dst[y:t+h , x:x+w]
cv.imwrite('fileResult2.jpg', dst)

# Reprojection Error
mean_error = 0

for i in range(len(objects)):
	imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
	error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
	mean_error += error
	
print( "total error: {}".format(mean_error/len(objpoints)))
