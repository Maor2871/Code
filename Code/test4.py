from test3 import ProportionalSplitter
import wx

class MainFrame(wx.Frame):

    def __init__(self,parent,id,title,position,size):
        wx.Frame.__init__(self, parent, id, title, position, size)

        ## example code that would be in your window's init handler:

        ## create splitters:
        self.split1 = ProportionalSplitter(self,-1, 0.66)
        self.split2 = ProportionalSplitter(self.split1,-1, 0.50)

        ## create controls to go in the splitter windows...

        ## add your controls to the splitters:
        self.split1.SplitVertically(self.split2, self.rightpanel)
        self.split2.SplitHorizontally(self.topleftpanel, self.bottomleftpanel)