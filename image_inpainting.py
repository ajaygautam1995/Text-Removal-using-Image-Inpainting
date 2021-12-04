import numpy as np
import cv2 as cv
import sys
import matplotlib.pyplot as plt
from skimage import data
from skimage.io import imread
"""creating mause handling class which will be using for 
creating live distortion on image.
in this class we will create constructor that will be usefull for
showing our image.
""" 

# OpenCV Utility Class for Mouse Handling
class Sketcher:
    def __init__(self, wind_name, destorted_set, colors_func):
        self.preserved_pt = None
        self.wind_name= wind_name
        self.destorted_set=destorted_set
        self.colors_func= colors_func
        self.dirty = False 
        self.show()
        cv.setMouseCallback(self.wind_name, self.mouse_handling)

    def show(self):
        cv.imshow(self.wind_name, self.destorted_set[0])
        cv.imshow(self.wind_name + ": mask", self.destorted_set[1])

    # onMouse function for Mouse Handling
    def mouse_handling(self, event, x_cor, y_cor, flags, parameters):
        points = (x_cor, y_cor)
        if event == cv.EVENT_LBUTTONDOWN:
            self.preserved_pt = points
        elif event == cv.EVENT_LBUTTONUP:
            self.preserved_pt = None

        if self.preserved_pt and flags & cv.EVENT_FLAG_LBUTTON:
            for dst, color in zip(self.destorted_set, self.colors_func()):
                cv.line(dst, self.preserved_pt, points, color, 5)
            self.dirty = True
            self.preserved_pt = points
            self.show()
"""
now we will creat main function
key: we have two algorithm  
1.NS algorithm
1. FMM algorithm(fast marching method)
 if we press key "t" then NS algorith will run
 and if we press key "N" then FMM algorithm will run.
 if we press key "r" then impaint mask will reset.
 if we press key "ESC" then our program will be reset
"""

def main():

    print("Usage: python inpaint <image_path>")
    print("Keys: ")
    print("press 't' for FMM")
    print("press 'n' for NS technique")
    print("press 'r' for reset the inpainting mask")
    print("press 'ESC' for  - exit")

    # Read image in color mode
 
    #in_img = cv.imread('/content/ground_truith.jpg', cv.IMREAD_COLOR)# IMREAD_COLOR is flag value that use for in which mode u want to read image
    in_img= data.camera() 
    """ sometime our system does not read image """
    # If image is not read properly, return error
    if in_img is None:
        print('Failed to load image file: {}'.format(in_img))
        return
    """now wew will creat mask on our original image. we will use copy function that
     is able to make the copy of image.
    """
    # Create a copy of original image
    masked_im = in_img.copy()
    # Create a black copy of original image
    # Acts as a mask
    inpainted_Mask = np.zeros(in_img.shape[:2], np.uint8)# it will create black image of original image size
    # Create sketch using OpenCV Utility Class: Sketcher
    sketch = Sketcher('image', [masked_im, inpainted_Mask], lambda : ((255, 255, 255), 255))
    """ now we will use key under infinite loop, that will
    use key for image impainting algorithm
    """
    while True:
        ch = cv.waitKey()
        if ch == 27: # 27 is ascii code for "ESC" key
            break
        if ch == ord('t'):
            # Use Algorithm proposed by Alexendra Telea: Fast Marching Method 
            res = cv.inpaint(src=masked_im, inpaintMask=inpainted_Mask, inpaintRadius=3, flags=cv.INPAINT_TELEA)#INPAINT_TELEA is name of fast marching method
            cv.imshow('Inpaint Output using FMM', res)
        if ch == ord('n'):
            # Use Algorithm proposed by Bertalmio, Marcelo, Andrea L. Bertozzi, and Guillermo Sapiro: Navier-Stokes, Fluid Dynamics, and Image and Video Inpainting (2001)
            res = cv.inpaint(src=masked_im, inpaintMask=inpainted_Mask, inpaintRadius=3, flags=cv.INPAINT_NS)
            cv.imshow('Inpaint Output using NS Technique', res)
        if ch == ord('r'):
            masked_im[:] = in_img
            inpainted_Mask[:] = 0
            sketch.show()

    print('Completed')


if __name__ == '__main__':
    main()
    cv.destroyAllWindows()