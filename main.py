import win32gui
import win32ui
import win32con
import win32api
import time
from random import random
import numpy as np
from matplotlib import pyplot 
from PIL import Image
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from key_map import keys

OUTPUT = "out.bmp"
WINDOW_NAME = "elpekenin"


def initialize_window():
    global SCREEN_WIDTH, SCREEN_HEIGHT, dcObj, cDC, dataBitMap, rect_left, rect_bottom, window
    # search window by name
    window = win32gui.FindWindow(None, WINDOW_NAME)

    # get window dimensions
    # pixels start counting on top-left corner
    rect = win32gui.GetWindowRect(window)
    rect_left, rect_top, rect_right, rect_bottom = rect[0:4]

    SCREEN_WIDTH, SCREEN_HEIGHT = rect_right - rect_left, rect_bottom - rect_top

    # create device context 
    windowDC = win32gui.GetWindowDC(window)  # DC = Device Context (int)
    dcObj = win32ui.CreateDCFromHandle(windowDC) # object from id
    cDC = dcObj.CreateCompatibleDC()

    # create bitmap
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, SCREEN_WIDTH, SCREEN_HEIGHT)

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

    b = np.array(remainder_dict[0]).reshape(SCREEN_HEIGHT, SCREEN_WIDTH)
    g = np.array(remainder_dict[1]).reshape(SCREEN_HEIGHT, SCREEN_WIDTH)
    r = np.array(remainder_dict[2]).reshape(SCREEN_HEIGHT, SCREEN_WIDTH)

    
    matrix = np.zeros((SCREEN_HEIGHT, SCREEN_WIDTH, 3))
    matrix[:,:,0] = r
    matrix[:,:,1] = g 
    matrix[:,:,2] = b 

    return matrix.astype(int)  


def click(x, y):
    """x,y coords starts at top left"""

    # Focus on window
    win32gui.SetForegroundWindow(window)

    # Take window position
    rect = win32gui.GetWindowRect(window)
    left, top = rect[0], rect[1]

    # Click it
    x += left
    y += top
    win32api.SetCursorPos((x,y))
    time.sleep(1)
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTDOWN,
        x,
        y,
        0,
        0
    )   
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTUP,
        x,
        y,
        0,
        0
    )

def trade(i):
    wait = 2 * random()
    x_off = int(100 * random())
    y_off = int(100 * random())

    if i == 0: # Start trading
        time.sleep(0.5) # wait before doing anything

        click( 60, 840) # open profile
        time.sleep(5) # wait for friend list to load

        click(300, 140) # open friend list if not open already
        time.sleep(5) # wait for friend list to load

        click(375, 250) # open search tool
        time.sleep(0.5) # wait for keyboard to load

        # type player's nickname
        for char in nick.lower():
            time.sleep(0.1)
            win32api.keybd_event(keys[char], 0,0,0)
            time.sleep(0.1)
            win32api.keybd_event(keys[char],0 ,win32con.KEYEVENTF_KEYUP ,0)

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
    cDC.BitBlt((0,0), (SCREEN_WIDTH, SCREEN_HEIGHT), dcObj, (0,0), win32con.SRCCOPY)

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
            text = "",
            hint_text = "Nickname of player2",
            size_hint = (GUI.text_x_size, GUI.text_y_size),
            pos_hint = {
                "x": 0.5 - GUI.text_x_size/2,
                "y":   3 * GUI.text_y_size
            },
            multiline = False
        )
        self.layout.add_widget(self.text_input_nick)

        self.text_input_tag_1 = TextInput(
            text = "",
            hint_text = "Tag name for player1",
            size_hint = (GUI.text_x_size, GUI.text_y_size),
            pos_hint = {
                "x": 0.5 - GUI.text_x_size/2,
                "y":   2 * GUI.text_y_size
            },
            multiline = False
        )
        self.layout.add_widget(self.text_input_tag_1)

        self.text_input_tag_2 = TextInput(
            text = "",
            hint_text = "Tag name for player2",
            size_hint = (GUI.text_x_size, GUI.text_y_size),
            pos_hint = {
                "x": 0.5 - GUI.text_x_size/2,
                "y":   1 * GUI.text_y_size
            },
            multiline = False
        )
        self.layout.add_widget(self.text_input_tag_2)

        self.start_button = Button(
            text="Start",
            size_hint = (0.3, 0.1),
            pos_hint = {"x": 0.6, "y": 0.2}
        )
        self.start_button.bind(on_press=self.start_trades)  
        self.layout.add_widget(self.start_button)

        # ===== Popup 
        self.error_layout = FloatLayout(size=(300,200))

        self.error_layout.add_widget(
            Label(
                text = "Check the input fields",
                size_hint = (0.3, 0.1),
                pos_hint = {"x": 0.35, "y": 0.5}
            )
        )

        self.close_popup_button = Button(
            text = "Close",
            size_hint = (0.3, 0.1),
            pos_hint = {"x": 0.35, "y": 0.1}
        )
        self.error_layout.add_widget(self.close_popup_button)
        self.error_popup = Popup(
            title = "Error",
            content = self.error_layout,
            size_hint=(None, None),
            size = (300,200)
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
