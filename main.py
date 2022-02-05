import win32gui
import win32ui
import win32con
import time
import random
import numpy as np
from matplotlib import pyplot 
from PIL import Image


OUTPUT = "out.bmp"
WINDOW_NAME = "elpekenin"


# ==================== Functions ====================
def cmyk_to_rgb(c, m, y, k):
    rgb_scale = 255.0
    cmyk_scale = 100.0

    # values in [-128, 127], so adding 128 converts to [0, 255]
    # c = np.array([bit+128 for index, bit in enumerate(image) if index%4 == 0])
    # m = np.array([bit+128 for index, bit in enumerate(image) if index%4 == 1])
    # y = np.array([bit+128 for index, bit in enumerate(image) if index%4 == 2])
    # k = np.array([bit+128 for index, bit in enumerate(image) if index%4 == 3])

    r = rgb_scale*(1-(c+k)/cmyk_scale)
    g = rgb_scale*(1-(m+k)/cmyk_scale)
    b = rgb_scale*(1-(y+k)/cmyk_scale)

    return r, g, b



# ==================== Initialize window variables ====================
# search window by name
window = win32gui.FindWindow(None, WINDOW_NAME)

# get window dimensions
rect = win32gui.GetWindowRect(window)
SCREEN_WIDTH, SCREEN_HEIGHT = rect[2] - rect[0], rect[3] - rect[1]

# create device context 
windowDC = win32gui.GetWindowDC(window)  # DC = Device Context (int)
dcObj = win32ui.CreateDCFromHandle(windowDC) # object from id
cDC = dcObj.CreateCompatibleDC()

# create bitmap
dataBitMap = win32ui.CreateBitmap()
dataBitMap.CreateCompatibleBitmap(dcObj, SCREEN_WIDTH, SCREEN_HEIGHT)

# bind device context to bitmap
cDC.SelectObject(dataBitMap)


# ==================== Ask info to user ====================
# nickname
# tag names


# ==================== Start trading ====================
# We assume both apps are already open with the secondary app on top-rigth 

# start
# open friend list
# search nickname on main app
# open trade
# secondary app goes into trade
# bot type their trade tags
# make 1st trade 

for _ in range(1):
    # check window 
        # something wrong -> close script 
    # re-open trade
    # trade

    # copy window image into bitmap
    cDC.BitBlt((0,0), (SCREEN_WIDTH, SCREEN_HEIGHT), dcObj, (0,0), win32con.SRCCOPY)

    # get bits of the image, 4 values for each pixel, 4th one is useless
    # python reads as signed int 8 bits, but they are actually unsigned
    bitMapValues = dataBitMap.GetBitmapBits()

    print(max(bitMapValues))

    remainder_dict = {
        0: [],
        1: [],
        2: [],
        3: [],
    }

    for index, value in enumerate(bitMapValues):
        remainder = index % 4
        fixed_value = value if value >= 0 else 255+value
        remainder_dict[remainder].append(fixed_value)

    b = np.array(remainder_dict[0]).reshape(SCREEN_HEIGHT, SCREEN_WIDTH)
    g = np.array(remainder_dict[1]).reshape(SCREEN_HEIGHT, SCREEN_WIDTH)
    r = np.array(remainder_dict[2]).reshape(SCREEN_HEIGHT, SCREEN_WIDTH)
    a = np.array(remainder_dict[3]).reshape(SCREEN_HEIGHT, SCREEN_WIDTH)

    
    matrix = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3))
    matrix[:,:,0] = r
    matrix[:,:,1] = g 
    matrix[:,:,2] = b 
    matrix = matrix.astype(int)

    Image.fromarray(matrix, mode="RGB").show()
    

    print(matrix.min())

    # matrix[:,:,3] = a

    pyplot.imshow(matrix)
    pyplot.show()

    # save bitmap to memory
    dataBitMap.SaveBitmapFile(cDC, OUTPUT)

# Free Resources
dcObj.DeleteDC()
cDC.DeleteDC()
win32gui.ReleaseDC(window, windowDC)
win32gui.DeleteObject(dataBitMap.GetHandle())