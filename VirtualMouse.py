import wx
from MoveMouse import MoveMouse
import sys
import os

class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="",
                    pos=(480, 200), size=wx.DefaultSize,
                    style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX,
                    name="MyFrame"):
        super(MyFrame, self).__init__(parent, id, title,
                                        pos, size, style, name)

        self.mouseThread = None

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        menubar = wx.MenuBar()

        # Run Menu
        runmenu = wx.Menu()
        item = wx.MenuItem(runmenu, wx.ID_ANY, "Run")
        self.Bind(wx.EVT_MENU, self.OnRun, item)
        runmenu.Append(item)
        menubar.Append(runmenu, "Run")

        # Stop Menu
        stopmenu = wx.Menu()
        item = wx.MenuItem(stopmenu, wx.ID_ANY, "Stop")
        self.Bind(wx.EVT_MENU, self.OnStop, item)
        stopmenu.Append(item)
        menubar.Append(stopmenu, "Stop")

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.SetInitialSize(size=(225, 50))        

    def OnRun(self, event):
        if not self.mouseThread:
            self.Iconize()
            self.mouseThread = MoveMouse(self)

    def OnStop(self, event):
        if self.mouseThread:
            self.mouseThread.abort()
            self.mouseThread = None

    def OnCloseWindow(self, e):    
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            if self.mouseThread:
                self.mouseThread.abort()
                self.mouseThread = None
                user.logout()
            self.Destroy()
            sys.exit(0)

class VirtualMouse(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Virtual Mouse")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = VirtualMouse(False)
    app.MainLoop()
