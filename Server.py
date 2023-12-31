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

    def __init__(self, server_host, server_port):
        """
        Initialize the Server instance.

        Attributes:
            server_socket (socket): The server's main socket.
            client_socket (socket): The socket for communicating with the client.
            address (tuple): The address of the connected client.
            logger (logging.Logger): The logger for recording server events.
        """
        
        self.logger = self.setup_logger()
        
        try:
            # Create a socket object
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Bind the socket to the host and port
            bind = server_host, server_port
            self.server_socket.bind(bind)
            
            # Listen for incoming connections
            self.server_socket.listen()
        except Exception as e:
            self.logger.error(f"Error during socket setup: {e}")
            print(f"Error during socket setup: {e}")
            raise
        
        try:
            # Accept a connection from the client
            self.client_socket, self.client_address = self.server_socket.accept()
        except Exception as e:
            self.logger.error(f"Error accepting connection: {e}")
            print(f"Error accepting connection: {e}")
            raise

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
    
    def action(self):
        self.command = "null"
        action = self.client_socket.recv(1024).decode()
        
        if action == "upload":
            file_name = self.client_socket.recv(1024).decode()
            self.receive_file(file_name)
            
        elif action == "download":
            file_name = self.client_socket.recv(1024).decode()
            
            self.send_file(file_name)
        else:
            self.command = "break"

    def receive_file(self, file_name):
        """
        Receive a file from the client and save it on the server.

        Parameters:
            file_name (str): The name of the file to be saved.
        """
        try:
            with open(f'{self.SERVER_FILES_PATH}\\{file_name}', "wb") as file:
                data = self.client_socket.recv(1024)
                # while data:
                #     data = self.client_socket.recv(1024)
                #     if not data:
                #         break
                file.write(data)
                
                # console
                print(f"\n    File '{file_name}' received successfully to server.")
                
                # server logger file
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
                
                # console
                print(f"\n    File '{file_name}' sent successfully from server.")
                
                # server logger file
                self.logger.info(f"File '{file_name}' sent successfully.")
        except Exception as e:
            self.logger.error(f"Error during file transmission: {e}")
            print(f"Error during file transmission: {e}")
            raise

    def close_connection(self):
        """
        Close the connection with the client.
        """
        try:
            if self.server_socket is not None:
                # Listen for incoming connections
                self.server_socket.listen()
            
                # Accept a connection from the client
                self.client_socket, self.client_address = self.server_socket.accept()
                while True:
                    s.action()
                    if s.command == "break":
                        break
        except Exception as e:
            print(f"Error closing server connection: {e}")
            self.logger.error(f"Error closing connection: {e}")
            raise

    def stop_server(self):
        """
        Close the server socket.
        """
        try:
            self.server_socket = None
            print("Server closed.")
        except Exception as e:
            print(f"Error closing server socket: {e}")
            self.logger.error(f"Error closing server socket: {e}")
            raise

if __name__ == "__main__":
    # Example usage:
    try:
        s = Server('127.0.0.1', 1234)
    
        while True:
            s.action()
            if s.command == "break":
                s.close_connection()
                break
        s.stop_server()
              

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
