from MyThread import MyThread
from ClientCommunicator import ClientCommunicator
from ExecutorCommunicator import ExecutorCommunicator
from ServerFileInit import FileInit
from Data_Base import DataBase
import select
import socket
import datetime
from Entities import Client, Executor


class GeneralVariables():
    """
        The attributes of this class don't have any other class to relate but they are necessary for the server.
    """

    def __init__(self):

        # All the clients that have signed to the system.
        self.clients = []

        # All the executors that have signed to the system.
        self.executors = []

        # All the sockets of the clients that have signed to the system.
        self.open_entities_sockets = []

        # The communication instance of the server.
        self.com = None

        # Creating the data base of the current client.
        self.data_base = DataBase("SystemData", "Cl9ass#if+ied", "lsdjkfn^gksfdog7#")

        # A list off all the requests that the server is currently handling.
        self.current_requests = []

        # The main code of the Server.
        self.main = None

    def get_client_by_socket(self, client_socket):
        """
            The function receives a socket of a signed client. Returns the client instance which the socket belongs to.
        """

        for client in self.clients:

            if client.socket is client_socket:

                return client

        return None

    def send(self, message):
        """
            The function transfer the message to the function which sends the message to other entities. Useful for
            cleaner code.
        """

        self.com.send.current_messages.append(message)


class Communication():
    """
        This class is responsible for everything relates to the communication with the others in the system.
    """

    def __init__(self, general_):

        self.general = general_

        self.socket = socket.socket()

        self.ip = "0.0.0.0"

        self.port = 7687

        self.socket.bind((self.ip, self.port))

        self.socket.listen(10)

        # The receive instance.
        self.receive = None

        # The send instance.
        self.send = None

    def start(self):
        """
            The function starts anything relates to the communication process.
        """

        # Create the send instance.
        self.send = Send(self)

        # Start thr start instance.
        self.send.start()

        # Create the receive instance.
        self.receive = Receive(self)

        # Start the receive instance.
        self.receive.start()

    def generate_socket(self):
        """
            The function generates new socket for a new client or executor.
        """

        # Create a new socket.
        new_socket = socket.socket()

        # Bind the new socket with the ip of the server but use different open port.
        new_socket.bind((self.ip, 0))

        new_socket.listen(1)

        return new_socket


class Receive(MyThread):
    """
        The class is responsible for anything relates to receiving data from others in the system. message
    """

    def __init__(self, communication_):

        MyThread.__init__(self, 1, "Receive")

        self.communication = communication_

        self.general = communication_.general

        # The main socket of the current server.
        self.socket = communication_.socket

        # The current message received.
        self.current_message = ""

        # Contains the socket of the entity which sent the current message.
        self.current_socket = None

        self.current_client = None

        self.current_executor = None

    def manager(self):
        """
            The function represents the main of the class.
        """

        while True:

            rlist, wlist, xlist = select.select([self.socket] + self.general.open_entities_sockets,
                                                self.general.open_entities_sockets, [])

            for entity_socket in rlist:

                # A new client or executor is trying to connect the server.
                if entity_socket is self.socket:

                    # Accept the client to the server.
                    (new_socket, address) = self.socket.accept()

                    # Make sure the entity which is trying to connect is new.
                    if new_socket not in self.general.open_entities_sockets:

                        self.current_socket = new_socket

                        data = self.current_socket.recv(1024)

                        if data == "New Message::Client":

                            self.sign_up_client()

                        elif data == "New Message::Executor":

                            self.sign_up_executor()

                # It's an already signed in entity, check what it wants.
                else:

                    # Update the current socket.
                    self.current_socket = entity_socket

                    # In case the client has disconnected or facing network problems.
                    try:

                        # Receives a new message from the current socket.
                        message = entity_socket.recv(1024)

                    # Continue to the next entity.
                    except:

                        continue

                    # convert the message to a list, each element is the title of the next one.
                    self.current_message = message.split("::")

                    # Send the message to follow_protocol which will direct it to the right part in the code according
                    # to the protocol rules.
                    self.follow_protocol()

    def follow_protocol(self):
        """
            The function follows the message by the protocol of the system.
        """

        message = self.current_message

        # Check if it's a client or an executor.
        if message[0] == "Client":

            pass

        elif message[0] == "Executor":

            pass

    def sign_up_client(self):
        """
            The function signs the socket in self.current_socket in to the system as a client. Creates a new thread
            that will communicate with him.
        """

        new_socket = self.current_socket

        # Add the socket of the client to the open_clients_socket list.
        self.general.open_entities_sockets.append(new_socket)

        # Create the new client a thread which he'll use to communicate with the server.
        client_communicator = ClientCommunicator(self.communication.generate_socket())

        # Create the new client.
        current_client = Client(self.general, new_socket, client_communicator)

        client_communicator.client = current_client

        # Add the new client to the system.
        self.general.clients.append(current_client)

        # Insert the client to the data base.
        self.general.main.new_clients_ids.append(current_client.id)

        # Notify the client that he is now connected to the server. Send him the new socket he'll communicate with.
        current_client.send_connected()

    def sign_up_executor(self):
        """
            The function signs the socket in self.current_socket in to the system as an executor. Creates a new thread
            that will communicate with him.
        """

        new_socket = self.current_socket

        # Add the socket of the executor to the open_entities_sockets list.
        self.general.open_entities_sockets.append(new_socket)

        # Create the new executor a thread which he'll use to communicate with the server.
        executor_communicator = ExecutorCommunicator(self.communication.generate_socket())

        # Create the new executor.
        current_executor = Executor(self.general, new_socket, executor_communicator)

        executor_communicator.executor = current_executor

        # Add the new client to the system.
        self.general.executors.append(current_executor)

        # Insert the entity to the data base.
        self.general.main.new_clients_ids.append(current_executor.id)

        # Notify the client that he is now connected to the server. Send him the new socket he'll communicate with.
        current_executor.send_connected()


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

                    # call the function which send the message.
                    self.send()

                self.current_messages = []

    def send(self):
        """
            The function sends the message in self.message to the entity in the system it should be sent to.
        """

        # The client to send the message to.
        client = self.message[0]

        # The message itself.
        content = self.message[1]

        # Send the content to the client.
        client.socket.send(content)


class Main(MyThread):

    def __init__(self, general_):

        MyThread.__init__(self, -1, "main")

        self.general = general_

        self.new_clients_ids = []

        self.new_executors_ids = []

    def manager(self):
        """
            The function runs the main code of the client as a thread.
        """

        # Create the files and directories of the system in the server.
        FileInit.init_files()

        # Connect to the data base.
        self.general.data_base.connect("System Data")

        self.build_data_base()

        # The instance this client is going to use in order to commit ant type of outside communication.
        general.com = Communication(general)

        # Start the communication thread. Receive and Send are beginning to operate in the background.
        general.com.start()

        while True:

            # Enter all the new entities to the data base.
            self.sign_up_new_entities_to_db()

            # Check if a client or executor has disconnected from the server or has a network problem. Disconnect him if
            # he does.
            self.look_for_disconnected_clients()
            self.look_for_disconnected_executors()

            # If there are new requests, add them to the requests to handle list.
            self.look_for_new_requests()

            # Handle all the requests that are currently waiting for the server for setting them up in the system.
            self.handle_requests()

    def look_for_new_requests(self):
        """
            The function iterates over all the connected clients and checks if a new request has received. If a new
            request has received, inserts it to the list that handles the request in the server.
        """

        for client in self.general.clients:

            if client.current_request:

                # Insert the new request to the list of the current requests the server has to handle.
                self.general.current_requests.append(client.current_request)

    def look_for_disconnected_clients(self):
        """
            The function checks if there are clients that are announced as disconnected so the connection with them has
            to be stopped.
        """

        for client in self.general.clients:

            if client.client_communicator.client_disconnected:

                client.disconnect()

    def look_for_disconnected_executors(self):
        """
            The function checks if there are executors that are announced as disconnected so the connection with them
            has to be stopped.
        """

        for executor in self.general.executors:

            if executor.executor_communicator.executor_disconnected:

                executor.disconnect()

    def handle_requests(self):
        """
            The function handles all the requests in the server.
        """

        # Iterate over all the requests that the server is currently handling.
        for request in self.general.current_requests:

            # Handle the request only if it have received properly.
            if request.full_request_has_arrived:

                # If the request hasn't been checked yet, check if it's valid.
                if not request.validation_checked:

                    request.check_validation()

                # If the request didn't dismantle yet, dismantle it.
                if not request.dismantled:

                    request.dismantle()

                # look for computers to run the requests on.
                if not request.executors:

                    request.find_executors()

                # The request is ready. If hasn't sent to the executors, send it.
                if not request.sent_to_executors:

                    request.send_to_executors()

    def build_data_base(self):
        """
            The function creates the tables of the databases and setting it up.
        """

        self.general.data_base.create_table("Clients", [["Id", "INT"], ["connected at", "TEXT"]])
        self.general.data_base.create_table("Executors", [["Id", "INT"], ["connected at", "TEXT"]])

    def sign_up_new_entities_to_db(self):
        """
            The function enters the new client to the data base.
        """

        for client_id in self.new_clients_ids:

            self.general.data_base.insert("Clients", [str(client_id), '"' + datetime.datetime.now().
                                          strftime("%I:%M%p on %B %d, %Y") + '"'])

        for executor_id in self.new_executors_ids:

            self.general.data_base.insert("Executors", [str(executor_id), '"' + datetime.datetime.now().
                                          strftime("%I:%M%p on %B %d, %Y") + '"'])


#-----Main Code-----#


# general is an instance that is going to contain many variables that are necessary in multiple areas in the code.
general = GeneralVariables()

general.main = Main(general)

general.main.start()