from MyThread import MyThread
import socket
from Request import ExecutorRequest, Request
import json


class ThreadCommunication():
    """
        This class is responsible for everything relates to the communication with the others in the system.
    """

    def __init__(self, general_, ip, port):

        self.general = general_

        # The socket of the main server.
        self.socket = socket.socket()

        self.ip = ip

        self.port = port

        self.socket.connect((self.ip, self.port))

        self.send = None

        self.receive = None

    def start(self):
        """
            The function starts anything relates to the communication process.
        """

        self.send = Send(self)

        self.send.start()

        self.receive = Receive(self)

        self.receive.start()

    def disconnected(self):
        """
            This function gets called when the server disconnects.
        """

        self.general.server_online = False


class Receive(MyThread):
    """
        The class is responsible for anything relates to receiving data from others in the system.
    """

    def __init__(self, communication_):

        MyThread.__init__(self, 1, "Receive")

        self.communicator = communication_

        self.communication = communication_

        self.general = communication_.general

        # The main socket of the current server.
        self.socket = communication_.socket

        # The current message received.
        self.current_message = ""

    def manager(self):
        """
            The function represents the main of the class.
        """

        while True:

            try:

                # Receives a new message from an entity in the system.
                messages = self.socket.recv(1024)

            except:

                self.communication.disconnected()
                return

            messages = messages.split("New Message::")

            for message in messages:

                self.current_message = message.split("::")
                print "New Message", self.current_message
                self.follow_protocol()

    def follow_protocol(self):
        """
            The function follows the message by the protocol of the system.
        """

        message = self.current_message

        if len(message) > 0 and message[0] == "Request":

            # The server wants to create new request.
            if len(message) > 2 and message[1] == "New Request":

                # Create a new request to execute.
                self.communicator.general.requests_to_execute.\
                    append(ExecutorRequest(message[2], "Requests_To_Execute/"))

            # The server is trying to upload another packet with an information about the current request.
            elif len(message) > 1 and message[1] == "Uploading":

                if len(message) > 3 and message[2] == "Request Dict":

                    # The dictionary of the request has received, create the current_request file to the current
                    # uploaded request.
                    Request.save_current_request(json.loads(message[3]),
                                                 self.general.requests_to_execute[-1].dir +
                                                 "/current_request.txt")

                # The server is sending more data about the file to run. append it to the already received data.
                elif len(message) > 3 and message[2] == "Run File":

                    message[3].replace("%~", "::")

                    self.general.requests_to_execute[-1].update_run_file(message[3])

                    # The file to run has fully received.
                    if len(message) > 4 and message[4] == "~~Finished Sending The File~~":

                        # Tell the server that the file has received and that he can send new data about the request.
                        self.communicator.send.current_messages.append("Request::Received::File To Run Has Received")

                # The server is sending more data about the current uploaded additional file.
                elif len(message) > 3 and message[2] == "Additional File":

                    message[3].replace("%~", "::")

                    self.general.requests_to_execute[-1].update_additional_file(message[3], message[4])

                    # The current uploaded additional file has fully received.
                    if len(message) > 5 and message[5] == "~~Finished Sending The File~~":

                        # Tell the server that the file has received and that he can send new data about the request.
                        self.communicator.send.current_messages.append("Request::Received::Additional File Has " +
                                                                       "Received")

                elif len(message) > 3 and message[2] == "Executors Amount" and message[3].isdigit():

                    self.general.requests_to_execute[-1].executors_amount = int(message[3])

            # The request to execute has just received from the server.
            elif len(message) > 1 and message[1] == "Finished Sending":

                self.general.requests_to_execute[-1].ready_to_execution = True


class Send(MyThread):
    """
         This class's instance sends anything which intended to be sent to other entities in the system.
    """

    def __init__(self, communication_):

        MyThread.__init__(self, 2, "Send")

        self.communication = communication_

        self.general = communication_.general

        # The main socket of the current Server.
        self.socket = communication_.socket

        # The current message this class has to send.
        self.current_messages = []

        # The current message the class sends. [client, content].
        self.message = []

    def manager(self):
        """
            The function represents the main of the class.
        """

        while True:

            # Check if the are messages to send.
            if self.current_messages:

                # Iterate over all the messages to send.
                for message in self.current_messages:
                    print "Sending:", message
                    self.message = message

                    # Send the content to the server thread as is.
                    self.socket.send("New Message::" + message)

                self.current_messages = []