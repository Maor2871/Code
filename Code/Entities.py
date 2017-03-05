class Client():
    """
        The class represent a client that has connected to the system.
    """

    # The id of the last client who has connected to the server.
    id = 0

    def __init__(self, general_, socket_, client_communicator):

        # The id of the client. The system uses this id in some cases in order to identify a client.
        self.id = Client.generate_id()

        # The socket of the client. With this socket the system can communicate with the client.
        self.socket = socket_

        # The thread that this server is using in order to communicate with the current client.
        self.client_communicator = client_communicator

        # Set the client's communicator the client itself.
        self.client_communicator.client = self

        # Contains variables that the class needs.
        self.general = general_

        # The current request of the client.
        self.current_request = None

        # Start the communicator of the client.
        self.client_communicator.start()

    @staticmethod
    def generate_id():
        """
            The function generates the next available id and returns it.
        """

        Client.id += 1

        return Client.id

    def send_connected(self):
        """
            The function sends the new client a message. This message tells him that he is now connected to the server
            and passes him the port that he'll use to communicate with his thread communicator.
        """

        self.general.send([self, "Client has connected properly::" +
                                 str(self.client_communicator.socket.getsockname()[1])])

    def disconnect(self):
        """
            The function disconnects the client from the server.
        """

        # Remove the client from the data base.
        self.general.data_base.remove("Computers", [['"' + "Id" + '"', str(self.id)]])

        self.general.current_requests.remove(self.current_request)
        self.general.open_clients_sockets.remove(self.socket)
        self.general.clients.remove(self)
        self.client_communicator.socket.close()
        self.client_communicator.client_socket.close()


class Executor():
    """
        The class represents an executor that has connected to the system.
    """

    # The id of the last executor who has connected to the server.
    id = 0

    def __init__(self, general_, socket_, executor_communicator):

         # The id of the executor. The system uses this id in some cases in order to identify an executor.
        self.id = Executor.generate_id()

        # The socket of the executor. With this socket the system can communicate with the executor.
        self.socket = socket_

        # The thread that this server is using in order to communicate with the current executor.
        self.executor_communicator = executor_communicator

        # Set the executor's communicator the executor itself.
        self.executor_communicator.client = self

        # Contains variables that the class needs.
        self.general = general_

        # The current request of the executor.
        self.current_request = None

        # Start the communicator of the executor.
        self.executor_communicator.start()

    @staticmethod
    def generate_id():
        """
            The function generates the next available id and returns it.
        """

        Executor.id += 1

        return Executor.id

    def send_connected(self):
        """
            The function sends the new executor a message. This message tells him that he is now connected to the server
            and passes him the port that he'll use to communicate with his thread communicator.
        """

        self.general.send([self, "Executor has connected properly::" +
                                 str(self.executor_communicator.socket.getsockname()[1])])

    def disconnect(self):
        """
            The function disconnects the executor from the server.
        """

        # Remove the executor from the data base.
        self.general.data_base.remove("Computers", [['"' + "Id" + '"', str(self.id)]])

        self.general.current_requests.remove(self.current_request)
        self.general.open_entities_sockets.remove(self.socket)
        self.general.executors.remove(self)
        self.executor_communicator.socket.close()
        self.executor_communicator.executor_socket.close()

    def can_execute(self, request):
        """
            The function checks if the executor has enough resources to execute the received request.
        """

        if request:
            return True