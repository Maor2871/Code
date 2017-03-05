import sys
from MyThread import MyThread
from FileInit import FileInit
from ExecutorMainCommunicator import MainCommunication
from ExecutorThreadCommunicator import ThreadCommunication
from RequestExecutor import RequestExecutor


#-----Classes-----#


class GeneralVariables():
    """
        The attributes of this class don't have any other class to relate but they are necessary for this executor.
    """

    def __init__(self):

        # The communication instance that has the ability to communicate with the main server.
        self.main_com = None

        # The communication instance that has the ability to communicate with the thread communicator of this executor
        # in the server.
        self.thread_com = None

        # All the requests that this executor has to execute.
        self.requests_to_execute = []

        # All the requests that this executor has to execute and their executors.
        # {request to execute: the request executor}
        self.current_requests = {}

        # True if the server isn't disconnected.
        self.server_online = True


class Main(MyThread):
    """
        This class contains all the main operations of this executor.
    """

    def __init__(self, general_):

        MyThread.__init__(self, -1, "main")

        self.general = general_

    def manager(self):
        """
            The function runs the main code of the executor as a thread.
        """

        # Setup all the files and folders that are necessary for this executor.
        FileInit.executor_init_files()

        # Setup the communication of this executor with the Main server of the system.
        self.general.main_com = MainCommunication(self.general, "192.168.0.243", 7687, self.create_thread_communicator)

        # Start all the defined threads.
        self.general.main_com.start()

        while True:

            # If the server has disconnected, close the executor.
            if not self.general.server_online:

                print "Server disconnected."
                sys.exit()

            # Iterate over all the requests this executor has to execute.
            for e_request in self.general.requests_to_execute:

                # The request is now ready to be sent to the vm.
                if e_request.ready_to_execution:

                    # Create an executor fot this request.
                    self.general.current_requests[e_request] = RequestExecutor(e_request, general)

                    # Start the request execution.
                    self.general.current_requests[e_request].start()

                    e_request.ready_to_execution = False

    def create_thread_communicator(self, ip, port):
        """
            The function receives a port and ip and creates the thread communicator.
        """

        self.general.thread_com = ThreadCommunication(self.general, ip, port)

        self.general.thread_com.start()


#-----Main Code-----#


general = GeneralVariables()

main = Main(general)

# Start the main code of the client.
main.start()