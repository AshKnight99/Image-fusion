import numpy as np
from skimage.color import rgb2gray, hsv2rgb, rgb2hsv, lab2rgb, rgb2lab
from skimage import img_as_ubyte
from merging_utilities.img_utils import *
from merging_utilities.os_utils import *

def therm_avg(rgb, thermal):

    # Split RGB values, not drop of alpha layer
    R,G,B = split_layers_to_3(rgb)
    
    avg_therm = avg_image(thermal)

    # create empty array, populate for new image
    # print(rgb.shape[2])
    rgbArray = np.zeros((rgb.shape[0],rgb.shape[1],3), 'uint8')
    rgbArray[..., 0] = avg_mat(R, avg_therm)
    rgbArray[..., 1] = avg_mat(G, avg_therm)
    rgbArray[..., 2] = avg_mat(B, avg_therm)

    return rgbArray

def thresh_layers_by_thermal(rgb, thermal, thresh=25):

    # Split RGB values, note: drop of alpha layer
    R,G,B = split_layers_to_3(rgb)
    
    avg_therm = avg_image(thermal)

    avg_therm = avg_therm > thresh
    
    # create empty array, populate for new image
    rgbArray = np.zeros((rgb.shape[0],rgb.shape[1],3), 'uint8')
    rgbArray[..., 0] = R*avg_therm
    rgbArray[..., 1] = G*avg_therm
    rgbArray[..., 2] = B*avg_therm

    return rgbArray

def repl_val_with_therm(rgb, thermal):
    # Split RGB values, note: drop of alpha layer
    # What is HSV: hue,saturation, value - works with lumonisty
    img_hsv = rgb2hsv(rgb)*255
    avg_therm = avg_image(thermal)
    
    H,S,V = split_layers_to_3(img_hsv)
    
    # print(np.amax(V))
    # print(np.amin(V))
    
    # create empty array, populate for new image
    newHSV = np.zeros((rgb.shape[0],rgb.shape[1],3), 'uint8')
    newHSV[..., 0] = H#*255
    newHSV[..., 1] = S#*255
    newHSV[..., 2] = avg_therm
    
    # print(np.amax(hsv2rgb(newHSV)))
    
    return img_as_ubyte(hsv2rgb(newHSV)) #in byte values - *255 

def repl_light_with_therm(rgb, thermal, illuminant='D65'):
    '''
    choose from these illuminants: ['A', 'D50', 'D55', 'D65', 'D75', 'E']
    '''
    # Split RGB values, note: drop of alpha layer
    img_lab = rgb2lab(rgb, illuminant='D65')
    avg_therm = avg_image(thermal)
    
    L,A,B = split_layers_to_3(img_lab)
    
    # set range to fit in LAB L range (0-100)  
    # X-axis: min value to max-value of average array, , Y- axis : 0-100
    avg_therm_scaled = np.interp(avg_therm, 
                       (avg_therm.min(), 
                        avg_therm.max()), 
                       (0, 100))
              
    print("\n Avg_thermal_scaled amax : "np.amax(avg_therm_scaled))
    # print(np.amin(avg_therm_scaled))


    # create empty array, populate for new image
    newLAB = np.zeros((rgb.shape[0],rgb.shape[1],3))
    newLAB[:,:, 0] = avg_therm_scaled #L
    newLAB[:,:, 1] = A #G
    newLAB[:,:, 2] = B #B
    
    newRGB = lab2rgb(newLAB)
    return img_as_ubyte(newRGB)