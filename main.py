import win32gui
import win32ui
import win32con
import win32api
import time
import numpy as np
from matplotlib import pyplot 
from PIL import Image
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import directkeys

# ====== YOU MIGHT NEED TO CHANGE THESE CONSTANTS
# name of your scrcpy window
WINDOW_NAME = "elpekenin"

# Positions measured on pixels from the top-left corner of the window
# if you have to change this, you can use paint to check the amount of pixels
PROFILE_POSITION = [60, 840] # your avatar face on bottom-left
FRIEND_POSITION = [300, 140] # friend list on the right side of your stats
SEARCH_POSITION = [375, 250] # search tool on friend list

# Your screen resolution in pixels, used to convert to & from windows coordinate system
SCREEN_SIZE = [1920, 1080]


def initialize_window():
    global window, WINDOW_WIDTH, WINDOW_HEIGHT, windowDC, dcObj, cDC, dataBitMap
    # search window by name
    window = win32gui.FindWindow(None, WINDOW_NAME)

    # get window dimensions
    # pixels start counting on top-left corner
    rect = win32gui.GetWindowRect(window)
    WINDOW_WIDTH, WINDOW_HEIGHT = rect[2] - rect[0], rect[3] - rect[1]

    # create device context 
    windowDC = win32gui.GetWindowDC(window)  # DC = Device Context (int)
    dcObj = win32ui.CreateDCFromHandle(windowDC) # object from id
    cDC = dcObj.CreateCompatibleDC()

    # create bitmap
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, WINDOW_WIDTH, WINDOW_HEIGHT)

    # bind device context to bitmap
    cDC.SelectObject(dataBitMap)


def free_resources():
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(window, windowDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())


def bitmap_to_np(bitMap):
    """
    Bitmap values are 4 data for each pixel (BGRA)
    Each data is a 8bit unsigned integer, but python reads as signed

    We 1st separate the 3 color channels
    If value < 0  -> undo the complement-2
    """

    remainder_dict = {
        0: [],
        1: [],
        2: [],
    }

    for index, value in enumerate(bitMap):
        remainder = index % 4
        if remainder == 3:
            continue
        fixed_value = value if value >= 0 else 255+value
        remainder_dict[remainder].append(fixed_value)

    b = np.array(remainder_dict[0]).reshape(WINDOW_HEIGHT, WINDOW_WIDTH)
    g = np.array(remainder_dict[1]).reshape(WINDOW_HEIGHT, WINDOW_WIDTH)
    r = np.array(remainder_dict[2]).reshape(WINDOW_HEIGHT, WINDOW_WIDTH)

    
    matrix = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3))
    matrix[:,:,0] = r
    matrix[:,:,1] = g 
    matrix[:,:,2] = b 

    return matrix.astype(int)  


def coords_to_pixels(x, y):
    "Coords [0, 65535], pixels depends on your screen"
    return int(x * SCREEN_SIZE[0]/65535), int(y * SCREEN_SIZE[1]/65535)


def pixels_to_coords(x, y):
    return int(x * 65535/SCREEN_SIZE[0]), int(y * 65535/SCREEN_SIZE[1])

 
def click(x, y):
    # Focus on window
    win32gui.SetForegroundWindow(window)

    # Check window position
    rect = win32gui.GetWindowRect(window)
    left, top = rect[0], rect[1]

    # Convert to local pixels (inside window)
    # To global pixels (inside computer screen)
    x += left
    y += top

    # Conver pixels to coords
    x, y = pixels_to_coords(x, y)

    # Newer function
    directkeys.press_click(x, y)


def trade(i):
    # In order to start trading we have to go on the friend list and search for the other player
    if i == 0:
        time.sleep(0.5) # wait before doing anything

        click(*PROFILE_POSITION) # open profile
        time.sleep(5) # wait for friend list to load

        click(*FRIEND_POSITION) # open friend list if not open already
        time.sleep(5) # wait for friend list to load

        click(*SEARCH_POSITION) # open search tool
        time.sleep(0.5) # wait for keyboard to load

        # type player's nickname
        for char in nick.lower():
            directkeys.press_key(char)

        # We assume both apps are already open with the secondary app on top-rigth 

        # start
        # open friend list
        # search nickname on main app
        # open trade
        # secondary app goes into trade
        # bot type their trade tags
        # make 1st trade 
        return

    # check window 
        # something wrong -> close script 
    # re-open trade
    # trade

    # copy window image into bitmap
    cDC.BitBlt((0,0), (WINDOW_WIDTH, WINDOW_HEIGHT), dcObj, (0,0), win32con.SRCCOPY)

    # read screen
    matrix = bitmap_to_np(dataBitMap.GetBitmapBits())

    # save bitmap to memory
    # dataBitMap.SaveBitmapFile(cDC, OUTPUT)

# GUI object
class GUI(App):
    text_x_size = 0.2
    text_y_size = 0.08


    def start_trades(self, *args, **kwargs):
        # check all 3 values are correct
        if "" in [self.text_input_nick.text, self.text_input_tag_1.text, self.text_input_tag_2.text]:
            self.error_popup.open()
            return     

        global nick
        nick = self.text_input_nick.text.rstrip()

        for i in range(99):
            trade(i)
            exit()
         
            # update progress bar
            progress_bar(i)

        # free resources
        exit()


    def build(self):
        # ===== Input dialog
        self.layout = FloatLayout(size=(500,500))

        self.text_input_nick = TextInput(
            text="",
            hint_text="Nickname of player2",
            size_hint=(GUI.text_x_size, GUI.text_y_size),
            pos_hint={
                "x": 0.5 - GUI.text_x_size/2,
                "y":   3 * GUI.text_y_size
            },
            multiline=False
        )
        self.layout.add_widget(self.text_input_nick)

        self.text_input_tag_1 = TextInput(
            text="",
            hint_text="Tag name for player1",
            size_hint=(GUI.text_x_size, GUI.text_y_size),
            pos_hint={
                "x": 0.5 - GUI.text_x_size/2,
                "y":   2 * GUI.text_y_size
            },
            multiline=False
        )
        self.layout.add_widget(self.text_input_tag_1)

        self.text_input_tag_2 = TextInput(
            text="",
            hint_text="Tag name for player2",
            size_hint=(GUI.text_x_size, GUI.text_y_size),
            pos_hint={
                "x": 0.5 - GUI.text_x_size/2,
                "y":   1 * GUI.text_y_size
            },
            multiline=False
        )
        self.layout.add_widget(self.text_input_tag_2)

        self.start_button = Button(
            text="Start",
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0.6, "y": 0.2}
        )
        self.start_button.bind(on_press=self.start_trades)  
        self.layout.add_widget(self.start_button)

        # ===== Popup 
        self.error_layout = FloatLayout(size=(300,200))

        self.error_layout.add_widget(
            Label(
                text="Check the input fields",
                size_hint=(0.3, 0.1),
                pos_hint={"x": 0.35, "y": 0.5}
            )
        )

        self.close_popup_button = Button(
            text="Close",
            size_hint=(0.3, 0.1),
            pos_hint={"x": 0.35, "y": 0.1}
        )
        self.error_layout.add_widget(self.close_popup_button)
        self.error_popup = Popup(
            title="Error",
            content=self.error_layout,
            size_hint=(None, None),
            size=(300,200)
        )
        self.close_popup_button.bind(on_press=self.error_popup.dismiss)

        return self.layout


def main():
    # Initialize window variables
    initialize_window()

    # Ask info to user 
    # nickname
    # tag names
    GUI().run()

    # We won't get there 
    free_resources()


if __name__ == "__main__":
    main()
