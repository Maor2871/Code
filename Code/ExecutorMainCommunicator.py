from MyThread import MyThread
import socket


class MainCommunication():
    """
        This class is responsible for everything relates to the communication with the others in the system.
    """

    def __init__(self, general_, ip, port, create_thread):

        self.general = general_

        # The socket of the main server.
        self.socket = socket.socket()

        # The ip of the main server.
        self.ip = ip

        # The port of the main server.
        self.port = port

        # Connect to the server.
        self.socket.connect((self.ip, self.port))

        # Tell the server that this is an executor.
        self.socket.send("New Message::Executor")

        # Every message that has to be delivered from this executor will be delivered by this instance.
        self.send = None

        # Every message from an instance in the system will be received by this instance.
        self.receive = None

        # The function that creates the thread communicator.
        self.create_thread = create_thread

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
                message = self.socket.recv(1024)

            except:

                self.communication.disconnected()
                break

            self.current_message = message.split("::")

            self.follow_protocol()

    def follow_protocol(self):
        """
            The function follows the message by the protocol of the system.
        """

        message = self.current_message

        if len(message) == 2 and message[0] == "Executor has connected properly" and message[1].isdigit():

            print "connected properly to the server."

            # Make sure there isn't already such a communicator.
            if not self.general.thread_com:

                # Create and start the thread communicator.
                self.communication.create_thread(self.communication.ip, int(message[1]))


class Send(MyThread):
    """
         This class's instance sends anything which intended to be sent to other entities in the system.
    """

    def __init__(self, communication_):

        MyThread.__init__(self, 2, "Send")

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

                    self.message = message

                    # call the function which sends the message.
                    self.send()

    def send(self):
        """
            The function sends the message in self.message to the entity in the system it should be sent to.
        """

        # The entity to send the message to.
        entity = self.message[0]

        # The message itself.
        content = self.message[1]

        # Send the content to the entity as is.
        entity.socket.send(content)
