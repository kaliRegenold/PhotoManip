# Author: Kali Regenold
# Date: 2018.10.07
# File: circles.py
# Takes an image in and return an image with circles of varying color, size,
# and thickness based on the average greyscale values of a given kernel size.
#
# There's really no good reason for this to be a class besides making it
# easier for me to program.


import cv2
import numpy
from sys import argv

# Trusted Arduino map function.
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# Class to handle in the in image, out image, and manipulation.
class CircleManip:

    def __init__(s, src_name, dest_name, kernel_size):
        s.src_name = src_name
        s.dest_name = dest_name
        s.kernel_size = kernel_size
        s.image_in = cv2.imread(src_name, 0)
        # Check if image opened.
        if s.image_in is None:
            raise FileNotFoundError('Cannot open src image.')
        s.height, s.width = s.image_in.shape

        # New white image of same dimensions.
        s.image_out = numpy.ones((s.height, s.width, 1), numpy.uint8)*255

    # Returns the sum of all values in the kernel.
    def getsum(s, i, j):
        sum = 0
        for x in range(0, s.kernel_size):
            for y in range(0, s.kernel_size):
                sum += s.image_in[i+x, j+y]
        return sum

    # Draw circles on image_out based on average values from image_in.
    def make_circles(s):
        # Step size is kernel size.
        for i in range(0, s.height-s.kernel_size, s.kernel_size):
            for j in range(0, s.width-s.kernel_size, s.kernel_size):
                # Get average value of kernel
                value = s.getsum(i, j)/(s.kernel_size**2)

                center = (j + int(s.kernel_size/2), i + int(s.kernel_size/2))
                # Radius and thickness are dependent on average value.
                # Change these for cool effects.
                radius =    map(255 - value, 0, 255, 1, int(s.kernel_size/2))
                thickness = map(255 - value, 0, 255, 1, int(s.kernel_size/2))

                # Draw the circle.
                cv2.circle(s.image_out, center, radius, value, thickness)

    def write_image(s):
        cv2.imwrite(s.dest_name, s.image_out)

    def show_image(s):
        cv2.imshow(s.dest_name, s.image_out)
        k = cv2.waitKey(0)
        if k == 27: # ESC
            cv2.destroyAllWindows()

def main():

    if len(argv) != 4:
        print("Usage: python3 circles.py <source_name> <dest_name> <kernel_size>")
        return

    source = argv[1]
    dest = argv[2]
    kernel = int(argv[3])

    c = CircleManip(source, dest, kernel)
    c.make_circles()
    c.write_image()

if __name__ == "__main__":
    main()
