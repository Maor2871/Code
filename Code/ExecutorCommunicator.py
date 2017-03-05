from MyThread import MyThread
from Request import ServerRequest
import json


class ExecutorCommunicator(MyThread):
    """
        The class represents a thread that is currently communicating with a specific executor.
    """

    def __init__(self, socket):

        MyThread.__init__(self, -1, "ExecutorCommunicator")

        # The socket which this thread is using to communicate with the executor.
        self.socket = socket

        # The socket of the executor that this thread is communicating with.
        self.executor_socket = None

        # The executor of this communicator.
        self.executor = None

        # The instance that is responsible for receiving the data from the executor.
        self.receive = None

        # The instance that is responsible for sending data to the executor.
        self.send = None

        # True if there is a problem connecting to the executor and the connection has to be stopped.
        self.executor_disconnected = False

    def manager(self):
        """
            The function manages the communication with the executor.
        """

        # Accept the executor.
        (new_socket, address) = self.socket.accept()

        self.executor_socket = new_socket

        # Create the instance that will receive the data from the executor.
        self.receive = Receive(self, self.executor_socket)

        # Start it.
        self.receive.start()

        # Create the instance that will send data to the executor.
        self.send = Send(self, self.executor_socket)

        # Start it.
        self.send.start()


class Receive(MyThread):
    """
        The class represents a thread that is listening for an executor.
    """

    def __init__(self, communicator, executor_socket):

        MyThread.__init__(self, -1, "ExecutorComReceive")

        # The communicator.
        self.communicator = communicator

        # The socket of the executor.
        self.executor_socket = executor_socket

    def manager(self):
        """
            The function is responsible for receiving data from the executor.
        """

        while True:

            # try:

                # Wait for data from the executor.
                message = self.executor_socket.recv(1024)

                messages = message.split("New Message::")

                for message in messages:
                    print "A new message from an executor", message
                    self.follow_protocol(message)

            # except:
            #
            #     self.communicator.executor_disconnected = True
            #     return

    def follow_protocol(self, message):
        """
            The function checks what the executor wants.
        """

        message = message.split("::")

        # Check if the executor is trying to send the server new information about a request he is executing.
        if len(message) > 0 and message[0] == "Request":

            if len(message) > 1 and message[1] == "Received":

                if len(message) > 2 and message[2] == "File To Run Has Received":

                    self.communicator.executor.current_request.received_file_to_run = True

                elif len(message) > 2 and message[2] == "Additional File Has Received":

                    self.communicator.executor.current_request.server_received_current_additional_file = True

            # The executor wants to send new output of a request.
            elif len(message) > 2 and message[1] == "New Output":

                new_output = message[2]
                self.communicator.executor.current_request.client.client_communicator.send.messages_to_send.\
                    append("Request::Status::New Output::" + new_output)

            # The executor wants to send a new error from a request.
            elif len(message) > 2 and message[1] == "New Error":

                pass


class Send(MyThread):
    """
        The class represents a thread that sends data to an executor.
    """

    def __init__(self, communicator, executor_socket):

        MyThread.__init__(self, -1, "executorComSend")

        self.executor_socket = executor_socket

        self.communicator = communicator

        # Contains the messages to send the executor.
        self.messages_to_send = []

    def manager(self):
        """
            The function responsible for sending data to the executor.
        """

        while True:

            if self.messages_to_send:

                # Iterate over all the messages that are supposed to be sent to the executor.
                for message in self.messages_to_send:

                    try:

                        # Send the message to the executor.
                        self.executor_socket.send("New Message::" + message)

                    except:

                        self.communicator.executor_disconnected = True

                self.messages_to_send = []