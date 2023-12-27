import socket
import logging

class Server:
    """
        The Server class implements a basic file transfer server using a client-server architecture.

        Usage:
            1. Create an instance of the Server class.
            2. Call the listen method to start listening for incoming connections.
            3. Accept client connections using the accept method.
            4. Use receive_file to receive a file from the client and save it on the server.
            5. Use send_file to send a file to the client.
            6. Close the connection with the client using close_connection.
            7. Stop the server using the stop_server method.

        Attributes:
            server_socket (socket): The server's main socket.
            client_socket (socket): The socket for communicating with the client.
            address (tuple): The address of the connected client.
            logger (logging.Logger): The logger for recording server events.
    """

    SERVER_FILES_PATH = 'C:\\Programming\\Server_Files'

    def __init__(self):
        """
        Initialize the Server instance.

        Attributes:
            server_socket (socket): The server's main socket.
            client_socket (socket): The socket for communicating with the client.
            address (tuple): The address of the connected client.
            logger (logging.Logger): The logger for recording server events.
        """
        self.server_socket = None
        self.client_socket = None
        self.address = None
        self.logger = self.setup_logger()

    def setup_logger(self):
        """
            Set up the logger for the server.

            Returns:
                logging.Logger: The configured logger.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y')

        file_handler = logging.FileHandler(f'{self.SERVER_FILES_PATH}\\server_log.txt')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger

    def listen(self, server_address, port):
        """
        Start listening for incoming connections on the specified address and port.

        Parameters:
            server_address (str): The IP address or hostname of the server.
            port (int): The port number on which the server is listening for connections.
        """
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bind = server_address, port
            self.server_socket.bind(bind)
            self.server_socket.listen()
        except Exception as e:
            self.logger.error(f"Error during socket setup: {e}")
            print(f"Error during socket setup: {e}")
            raise

    def accept(self):
        """
        Accept a connection from a client.
        """
        try:
            self.client_socket, self.address = self.server_socket.accept()
        except Exception as e:
            self.logger.error(f"Error accepting connection: {e}")
            print(f"Error accepting connection: {e}")
            raise

    def receive_file(self, file_name):
        """
        Receive a file from the client and save it on the server.

        Parameters:
            file_name (str): The name of the file to be saved.
        """
        try:
            with open(f'{self.SERVER_FILES_PATH}\\{file_name}', "wb") as file:
                print(f"Receiving file: {file_name}")
                data = self.client_socket.recv(1024)
                # while True:
                #     data = self.client_socket.recv(1024)
                #     if not data:
                #         break
                file.write(data)
                print(f"File '{file_name}' received successfully.")
                self.logger.info(f"File '{file_name}' received successfully.")
        except Exception as e:
            self.logger.error(f"Error during file reception: {e}")
            print(f"Error during file reception: {e}")
            raise

    def send_file(self, file_name):
        """
        Send a file to the client.

        Parameters:
            file_name (str): The name of the file to be sent.
        """
        try:
            with open(f'{self.SERVER_FILES_PATH}\\{file_name}', "rb") as file:
                data = file.read()
                self.client_socket.sendall(data)
                
                self.logger.info(f"File '{file_name}' sent successfully.")
                print(f"File '{file_name}' sent successfully.")
        except Exception as e:
            self.logger.error(f"Error during file transmission: {e}")
            print(f"Error during file transmission: {e}")
            raise

    def close_connection(self):
        """
        Close the connection with the client.
        """
        try:
            self.client_socket.close()
        except Exception as e:
            self.logger.error(f"Error closing connection: {e}")
            print(f"Error closing connection: {e}")
            raise

    def stop_server(self):
        """
        Close the server socket.
        """
        try:
            self.server_socket.close()
        except Exception as e:
            self.logger.error(f"Error closing server socket: {e}")
            print(f"Error closing server socket: {e}")
            raise

# Example usage:
try:
    s1 = Server()
    s1.listen('127.0.0.1', 8080)
    s1.accept()

    # Example of reusing the socket for multiple file transfers
    s1.receive_file('received_file.txt')
    s1.send_file('received_file.txt')

    # s1.receive_file('received_file_2.txt')
    # s1.send_file('received_file_2.txt')

    s1.close_connection()
    s1.stop_server()

except Exception as e:
    print(f"An unexpected error occurred: {e}")