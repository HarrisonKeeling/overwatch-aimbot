import cv2
from math import pow, sqrt
from mss import mss
import numpy as np

from win32 import win32api
import win32con

import lib.viz as viz

if __debug__:
    cv2.namedWindow('res', cv2.WINDOW_NORMAL)

# The size of the window to scan for targets in, in pixels
# i.e. SQUARE_SIZE of 600 => 600 x 600px
SQUARE_SIZE = 600
viz.SQUARE_SIZE = SQUARE_SIZE

# The maximum possible pixel distance that a character's center
# can be before locking onto them
TARGET_SIZE = 100
MAX_TARGET_DISTANCE = sqrt(2 * pow(TARGET_SIZE, 2))
viz.TARGET_SIZE = TARGET_SIZE
viz.MAX_TARGET_DISTANCE = MAX_TARGET_DISTANCE

# Create an instance of mss to capture the selected window square
sct = mss()

# Use the first monitor, change to desired monitor number
dimensions = sct.monitors[1]

# Compute the center square of the screen to parse
dimensions['left'] = int((dimensions['width'] / 2) - (SQUARE_SIZE / 2))
dimensions['top'] = int((dimensions['height'] / 2) - (SQUARE_SIZE / 2))
dimensions['width'] = SQUARE_SIZE
dimensions['height'] = SQUARE_SIZE


# Calls the Windows API to simulate mouse movement events that are sent to OW
def mouse_move(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)


# Determines if the Caps Lock key is pressed in or not
def is_activated():
    return win32api.GetAsyncKeyState(0x14) != 0


def locate_target(target):
    # compute the center of the contour
    moment = cv2.moments(target)
    if moment["m00"] == 0:
        return

    cx = int(moment["m10"] / moment["m00"])
    cy = int(moment["m01"] / moment["m00"])

    mid = SQUARE_SIZE / 2
    x = -(mid - cx) if cx < mid else cx - mid
    y = -(mid - cy) if cy < mid else cy - mid

    target_size = cv2.contourArea(target)
    distance = sqrt(pow(x, 2) + pow(y, 2))

    # There's definitely some sweet spot to be found here
    # for the sensitivity in regards to the target's size
    # and distance
    slope = ((1.0 / 3.0) - 1.0) / (MAX_TARGET_DISTANCE / target_size)
    multiplier = ((MAX_TARGET_DISTANCE - distance) / target_size) * slope + 1

    if is_activated():
        mouse_move(int(x * multiplier), int(y * multiplier))

    if __debug__:
        # draw the contour of the chosen target in green
        cv2.drawContours(frame, [target], -1, (0, 255, 0), 2)
        # draw a small white circle at their center of mass
        cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1)


# Main lifecycle
while True:
    frame = np.asarray(sct.grab(dimensions))
    contours = viz.process(frame)

    # For now, just attempt to lock on to the largest contour match
    if len(contours) > 1:
        # contour[0] == bounding window frame
        # contour[1] == closest/largest character
        locate_target(contours[1])

    if __debug__:
        # Green contours are the "character" matches
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
        cv2.imshow('res', frame)

    # Press `q` to stop the program
    if cv2.waitKey(25) & 0xFF == ord("q"):
            break

sct.close()
cv2.destroyAllWindows()
