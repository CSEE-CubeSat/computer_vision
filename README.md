Here we store python scripts that do cool stuff


Our python libraries are installed in a venv (virtual environment), which is essentially a easily customizeable
version of python inside our /home/ folder.

To start, run:

$ source venv/bin/activate

This activates the venv and any scripts you run will use the packages installed inside the venv.

make sure you cd into: (venv) mist@raspberrypi:~/MIST $

then run any script in the /MIST/ folder by running:

$ python myscript.py

_______________________________________________________
WHAT DO THE SCRIPTS DO?

$ python imagetest.py

A test script to load an image. Currently loads goose.jpg from the /images/ folder.
___________

$ python cameratest.py

A test script that takes a picture. Must have the Raspberry Pi Camera plugged into the camera slot.
If the raspi camera still isnt detected, restart the pi with it plugged in

___________

$ python arucotest.py

A script that generates an ArUco marker, and saves it in the images folder. To generate a new ArUco marker,
open the file in Geany and change the ID number and file name to a different integer number.

___________

$ python markerDetector.py --image images/___.jpg --type DICT_6X6_250

A script that scans the image you input for 6X6_250 ArUco markers. Don't worry, 6X6_250 is the only kind we 
have generated. It shows a new version of the image with added drawings, you must save this version manually.

___________

$ python detect_aruco_video.py --type DICT_6X6_250

Starts a video stream and checks each frame for ArUco markers. Press Q to stop video.

___________

$ python cameraCalibration

Uses an image of a 9x6 chessboard pattern to determin the intrinsic parameters of the camera and corrects 
distortion of the camera if caused by camera lense