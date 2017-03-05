from MyThread import MyThread
from subprocess import Popen, PIPE, STDOUT


class RequestExecutor(MyThread):
    """
        The class instances are responsible for anything relates to their requests execution.
    """

    def __init__(self, request, general_):

        MyThread.__init__(self, -1, "Request Executor")

        # The request this instance is currently handling.
        self.request = request

        # The connector to the main executor script.
        self.general = general_

        # The process of the running file.
        self.process = None

    def manager(self):
        """
            The function that manages anything relates to the request execution.
        """

        self.process = Popen("python " + self.request.dir + self.request.file_to_run, shell=True, stdout=PIPE,
                             stderr=STDOUT)

        stdout = []

        while True:

            line = self.process.stdout.readline()

            if line == '':

                break

            else:
                if line != "\n":

                    stdout.append(line)

                    self.general.thread_com.send.current_messages.append("Request::New Output::" + line)
