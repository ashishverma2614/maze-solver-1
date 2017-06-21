
# import the necessary packages
import numpy as np
from skimage import exposure
import argparse
import glob
import cv2
import imutils
from PIL import Image
import PIL.ImageOps  

def auto_canny(image, sigma=0.33):
	# compute the median of the single channel pixel intensities
	v = np.median(image)

	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)

	# return the edged image
	return edged

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread("input/image_0009.jpg")
original_ratio = image.shape[0] / 600.0
orig = image.copy()
image = imutils.resize(image, height = 600)

#PROCESS
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)

	# apply Canny edge detection using a wide threshold, tight
	# threshold, and automatically determined threshold
	#wide = cv2.Canny(blurred, 10, 200)
	#tight = cv2.Canny(blurred, 225, 250)
autoedge = auto_canny(blurred)
	#break

# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
(cnts, _) = cv2.findContours(autoedge.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None


# loop over our contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# if our approximated contour has four points, then
	# we can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break

# now that we have our screen contour, we need to determine
# the top-left, top-right, bottom-right, and bottom-left
# points so that we can later warp the image -- we'll start
# by reshaping our contour to be our finals and initializing
# our output rectangle in top-left, top-right, bottom-right,
# and bottom-left order
pts = screenCnt.reshape(4, 2)
rect = np.zeros((4, 2), dtype = "float32")

# the top-left point has the smallest sum whereas the
# bottom-right has the largest sum
s = pts.sum(axis = 1)
rect[0] = pts[np.argmin(s)]
rect[2] = pts[np.argmax(s)]

# compute the difference between the points -- the top-right
# will have the minumum difference and the bottom-left will
# have the maximum difference
diff = np.diff(pts, axis = 1)
rect[1] = pts[np.argmin(diff)]
rect[3] = pts[np.argmax(diff)]

# multiply the rectangle by the original ratio
rect *= original_ratio

# now that we have our rectangle of points, let's compute
# the width of our new image
(tl, tr, br, bl) = rect
widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

# ...and now for the height of our new image
heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

# take the maximum of the width and height values to reach
# our final dimensions
maxWidth = max(int(widthA), int(widthB))
maxHeight = max(int(heightA), int(heightB))

# construct our destination points which will be used to
# map the screen to a top-down, "birds eye" view
dst = np.array([
	[0, 0],
	[maxWidth - 1, 0],
	[maxWidth - 1, maxHeight - 1],
	[0, maxHeight - 1]], dtype = "float32")

# calculate the perspective transform matrix and warp
# the perspective to grab the screen
M = cv2.getPerspectiveTransform(rect, dst)
warp = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))
warp = cv2.resize(warp, (1200, 1200)) 
warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
ret,binary = cv2.threshold(warp,127,255,cv2.THRESH_BINARY)


cv2.imwrite("output/cropped.jpg",binary)
#cv2.imshow("original", image)
#cv2.imshow("wrapped", binary)



#####DISPLAY SECTION BREAK (for testing purpose)#####
# show the images
#cv2.imshow("Original", image)

#cv2.imshow("Edges", autoedge)

#cv2.drawContours(image, [screenCnt], 0, (0, 255, 0), 3)

#cv2.namedWindow("test", cv2.WINDOW_NORMAL)
#cv2.resizeWindow('test', 600,600)
#cv2.imshow("test", image)

# create a mask for the scree
#mask = np.zeros(image.shape[:2], dtype = "uint8")
#cv2.drawContours(mask, [screenCnt], -1, 255, -1)
#cv2.imshow("Masked", cv2.bitwise_and(image, image, mask = mask))


#end
#cv2.waitKey(0)