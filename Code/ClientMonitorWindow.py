import wx
from wx.lib.splitter import MultiSplitterWindow
from Colours import Colours
from Monitor import Monitor


class ClientMonitorWindow(wx.Panel):
    """
        The monitor window of the client gui.
    """

    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.SetBackgroundColour(Colours.main_window)

        # The widget that's responsible on showing the multiple monitors together.
        self.monitors_splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)

        # The number of executors that are currently sends data about the running file.
        self.executors_count = 0

        self.executors_monitors = []

        # Create a title that will notify the user that he has to execute a request in order to see monitors.
        self.startup_title = wx.StaticText(self, -1, 'You have to start a request in order to use the monitors.')
        self.startup_title.SetFont(wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        self.startup_title.SetForegroundColour(Colours.main_title)

        # self.text_box = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        # self.text_box.SetBackgroundColour(Colours.text_ctrl)
        #
        # sizer = wx.BoxSizer()
        #
        # sizer.Add(self.text_box, 0, wx.ALL | wx.EXPAND, 5)
        #
        # self.SetSizer(sizer)

    def setup(self):
        """
            The function setups the monitor according to its attributes.
        """

        # Create a monitor for each executor.
        for i in range(self.executors_count):

            # Create the monitor.
            self.executors_monitors.append(Monitor(self.monitors_splitter, self.executors_count))

            # Append it to the splitter.
            self.monitors_splitter.AppendWindow(self.executors_monitors[self.executors_count - 1])

        self.Show()

    def new_output(self, new_output, executor_id):
        """
            The function updates the received output in the textbox.
        """

        self.executors_monitors[executor_id].output_box.append_value(new_output)