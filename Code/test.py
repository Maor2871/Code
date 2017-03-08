import wx
from wx.lib.splitter import MultiSplitterWindow

########################################################################
class SamplePanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, colour):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(colour)

########################################################################

class MainPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)

        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)

        left_panel = SamplePanel(splitter, "grey")
        right_panel = SamplePanel(splitter, "blue")
        panel = SamplePanel(self, "yellow")

        splitter.SplitVertically(left_panel, right_panel)
        splitter.SetMinimumPaneSize(200)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)

        sizerp = wx.BoxSizer(wx.VERTICAL)
        sizerp.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetSizer(sizerp)


class MainFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="MultiSplitterWindow Tutorial")

        self.main_panel = MainPanel(self)

        self.Show()
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
