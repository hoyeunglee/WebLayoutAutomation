#I am retired old programmer and decide not to scratch any more
#This program is to demonstrate shape detector can do layout of web
#This is just a proof of concept program
#python unfinished_detect_shapes.py --image weblayout2.png
import argparse
import imutils
import cv2
class ShapeDetector:
	def __init__(self):
		pass
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = ["unidentified",(0,0,0,0)]
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = ["triangle",(0,0,0,0)]
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = ["square",(x, y, w, h)] if ar >= 0.95 and ar <= 1.05 else ["rectangle",(x, y, w, h)]
		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = ["pentagon",(0,0,0,0)]
		# otherwise, we assume the shape is a circle
		else:
			shape = ["circle",(0,0,0,0)]
		# return the name of the shape
		return shape

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=1400)
ratio = image.shape[0] / float(resized.shape[0])
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print("test0")
sd = ShapeDetector()
print("test1")
file1 = open("weblayout.html","w")
file1.write("<html>\n")
file1.write("<head>\n")
file1.write("</head>\n")
file1.write("<body>\n")
file1.write("<table border=1 width=\"100%\" height=\"100%\">")
# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)
	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv2.putText(image, shape[0], (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)
	print(shape[0])
	file1.write("<tr>\n")
	file1.write("<td width=\""+str(shape[1][2])+"\" height=\""+str(shape[1][3])+"\">\n")
	file1.write("</td>\n")
	#<td width="80%" height="100%">
	#</td>
	file1.write("</tr>")
	# show the output image
	cv2.imshow("Image", image)
	cv2.waitKey(0)

file1.write("</table>\n")
file1.write("</body>\n")
file1.write("</html>\n")
file1.close()