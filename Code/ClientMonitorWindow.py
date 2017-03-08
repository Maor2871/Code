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
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.splitter.SetMinimumPaneSize(100)
        self.splitter_main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.splitter_main_sizer.Add(self.splitter, 1, wx.EXPAND)

        # The panel that shows on startup when the server haven't sent data from an executor yet.
        self.start_up_panel = wx.Panel(self)
        self.start_up_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.start_up_panel_sizer.Add(self.start_up_panel, 1, wx.EXPAND)

        # Panel that is being used when only one executor is set up.
        self.one_monitor_panel = wx.Panel(self)
        self.one_monitor_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.one_monitor_panel_sizer.Add(self.one_monitor_panel, 1, wx.EXPAND)

        # Set the current sizer of the window to the startup sizer.
        self.SetSizer(self.start_up_panel_sizer)

        # The number of executors that are currently sends data about the running file.
        self.executors_count = 0

        # A dict of all the executors that have a monitor and their monitor. {executor id: monitor}
        self.executors_monitors = {}

        # The title that will be shown to the user at startup.
        self.startup_title = None

        # Initialize the start up screen.
        self.start_up()

    def check_new_executor(self, executor_id):
        """
            The function checks if that executor already has a monitor, if he doesn't creates him one.
        """

        # Check if it's a new executor so he doesn't have a monitor.
        if not executor_id in self.executors_monitors:

            # Create the monitor.
            self.executors_monitors[executor_id] = Monitor(self, self.executors_count)
            #
            # # Increase the counter.
            # self.executors_count += 1
            #
            # # Refresh the monitors structure to add the new monitor.
            # self.refresh_monitors()

    def refresh_monitors(self):
        """
            The function is being called when a changes has been made an the monitors structure should get changed.
        """

        # If True that executor is the only one to get a window.
        if len(self.executors_monitors) == 1:
            pass
            # # Set the panel of the executor to the panel of the single monitor.
            # self.one_monitor_panel = self.executors_monitors.values()[0]

            # # Set the sizer of the monitors window to the single monitor panel.
            # self.SetSizer(self.one_monitor_panel_sizer)

        else:

            left_panel = Monitor(self.splitter, 0)
            right_panel = Monitor(self.splitter, 1)

            self.splitter.SplitVertically(left_panel, right_panel)

    def start_up(self):
        """
            The function is responsible on anything relates to the startup page.
        """

        # Create a title that will notify the user that he has to execute a request in order to see monitors.
        self.startup_title = wx.StaticText(self.start_up_panel, -1, 'You have to start a request in order to use the'
                                                                    ' monitors.')
        self.startup_title.SetFont(wx.Font(30, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        self.startup_title.SetForegroundColour(Colours.main_title)

    def new_output(self, new_output, executor_id):
        """
            The function updates the received output in the textbox.
        """

        # First, check if this executor has a monitor. If he doesn't, create him one.
        self.check_new_executor(executor_id)

        # Append the received new output to the output box of the current executor monitor.
        self.executors_monitors[executor_id].output_box.append_value(new_output)