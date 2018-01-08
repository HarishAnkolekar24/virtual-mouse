import numpy as np
import cv2
from skimage.measure import label, regionprops
import pyautogui, sys
import math
from threading import *
import wx

EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win, func):
    """Define Result Event."""
    win.Connect(-1, -1, EVT_RESULT_ID, func)

class ResultEvent(wx.PyEvent):
    """Simple event to carry arbitrary result data."""
    def __init__(self, data):
        """Init Result Event."""
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_RESULT_ID)
        self.data = data

class MoveMouse(Thread):
    def __init__(self, notify_window):
        Thread.__init__(self)
        self._notify_window = notify_window
        self._want_abort = 0
        self.leftClicked = 0
        self.doubleClicked = 0
        self.start()

    def run(self):
        cap = cv2.VideoCapture(0)
            
        try:
            while True:

                if self._want_abort:
                    wx.PostEvent(self._notify_window, ResultEvent(None))
                    return

                ret, img = cap.read()
                img = cv2.flip(img, 1)

                gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                b = img[:,:,0]
                g = img[:,:,1]
                r = img[:,:,2]

                b_comp = cv2.subtract(b, gray_image)
                g_comp = cv2.subtract(g, gray_image)
                r_comp = cv2.subtract(r, gray_image)
                
                b_comp = cv2.medianBlur(b_comp, 5)
                g_comp = cv2.medianBlur(g_comp, 5)
                r_comp = cv2.medianBlur(r_comp, 5)

                ret, b_comp = cv2.threshold(b_comp, 46, 255, cv2.THRESH_BINARY)
                ret, g_comp = cv2.threshold(g_comp, 20, 255, cv2.THRESH_BINARY)
                ret, r_comp = cv2.threshold(r_comp, 46, 255, cv2.THRESH_BINARY)

                b_comp = cv2.morphologyEx(b_comp, cv2.MORPH_CLOSE, (5,5))
                g_comp = cv2.morphologyEx(g_comp, cv2.MORPH_CLOSE, (5,5))
                r_comp = cv2.morphologyEx(r_comp, cv2.MORPH_CLOSE, (5,5))

                b_comp_labeled = label(b_comp)
                g_comp_labeled = label(g_comp)
                r_comp_labeled = label(r_comp)

                yr = 0
                xr = 0
                pyautogui.FAILSAFE = False
                
                for r_region in regionprops(r_comp_labeled):
                    if r_region.area < 200:
                        continue

                    yrr, xrr = r_region.centroid
                    pyautogui.moveTo(xrr*4-400, yrr*4-400)        

                    for b_region in regionprops(b_comp_labeled):
                        if b_region.area < 500:
                            continue
                        
                        ybb, xbb = b_region.centroid

                        if (abs(yrr-ybb)<=200 and abs(xrr-xbb)<=200) and self.leftClicked==0 :
                            self.leftClicked = 1
                            pyautogui.click(button='left')
                        else:
                            self.leftClicked = 0
                            
                    for g_region in regionprops(g_comp_labeled):
                        if g_region.area < 500:
                            continue
                        
                        ygg, xgg = g_region.centroid

                        if (abs(yrr-ygg)<=200 and abs(xrr-xgg)<=200) and self.doubleClicked==0 :
                            self.doubleClicked = 1
                            pyautogui.doubleClick()
                        else:
                            self.doubleClicked = 0

                    yr = yrr
                    xr = xrr
                    self.leftClicked = 0
                    self.doubleClicked = 0
                
        finally:
            cap.release()
            cv2.destroyAllWindows()    

    def abort(self):
        self._want_abort = 1