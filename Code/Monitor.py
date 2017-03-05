import wx
from Colours import Colours


class Monitor(wx.Panel):
    """
        The instances of this class are monitors that show the data received from the executors.
    """

    def __init__(self, parent, executor_id):

        wx.Panel.__init__(self, parent=parent, id=executor_id)

        # Set the colour of the monitor.
        self.SetBackgroundColour(Colours.monitor)

        # The id of the monitor.
        self.id = executor_id

        # The output box of the monitor.
        self.output_box = OutputBox(self)


class OutputBox(wx.TextCtrl):
    """
        The class represents the output box of the monitor.
    """

    def __init__(self, parent):

        wx.TextCtrl.__init__(self, parent=parent, id=-1)

        # The content of the box.
        self.content = ""

    def append_value(self, value):
        """
            The function appends the received string and appends it to the box content and the box itself.
        """

        self.content += value

        self.SetValue(self.content)

    def new_value(self, value):
        """
            The function replaces the current content of the box with the received value and updates the box.
        """

        self.content = value

        self.SetValue(self.content)