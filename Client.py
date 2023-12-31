import socket  # Imports the socket library for network communication
import logging  # Imports the logging library for logging events

class Client:
    

    """
        A simple client class for file transfer using a client-server architecture.

        Attributes:
            BUFFER_SIZE (int): Constant for the buffer size used in file transfer.
            CLIENT_FILES_PATH (str): Path to the directory for client files.
            client_socket (socket.socket): The socket object for communication.
            logger (logging.Logger): The logger for recording events.

        Methods:
            __init__(): Initializes a new Client instance.
            connect_to_server(server_address, port): Initiates a connection with a server.
            send_file(file_name=DEFAULT_FILE_NAME): Transmits a file to the server.
            receive_file(file_name=DEFAULT_FILE_NAME): Receives a file from the server and saves it.
            close_connection(): Terminates the connection with the server.
    """

    
    BUFFER_SIZE = 1024  # Constant for the buffer size
    CLIENT_FILES_PATH = 'C:\\Programming\\Client_Files' # change it to the place you want to save the files
    counter = 1
    
    def __init__(self):
        
        """
            Purpose: Initializes a new Client instance.

            Parameters: None

            Actions:
                * Creates a socket object for communication.
                * Sets up the logger for recording events.
        """

        # Initialize a socket for communication
        self.client_socket = None
        self.logger = self.setup_logger()
        
    
    def setup_logger(self):
        """
            Purpose: Sets up the logger for the client.

            Parameters: None

            Actions:
                * Configures the logger with appropriate settings.
                * Returns the configured logger object.
             Returns:
                logging.Logger: The configured logger.    
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m-%Y')

        file_handler = logging.FileHandler(f'{self.CLIENT_FILES_PATH}\\client_log.txt')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        return logger   
        

    def connect_to_server(self, server_address, port):
        """
            Purpose: Initiates a connection with a server.

            Parameters:
                * server_address (str): The IP address or hostname of the server.
                * port (int): The port number on which the server is listening for connections.

            Actions:
                * Creates a socket object.
                * Connects the socket to the specified server_address and port.
        """     

        try:
            # Create a tuple containing the server address and port
            connect = (server_address, port)
            
            # Initialize the socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Attempt to connect to the server
            self.client_socket.connect(connect)
            
            # Connection successful
            self.logger.info("Connected to the server.")
            print("\nConnected to the server.")
        except ConnectionRefusedError:
            # Handle connection refusal (server not running)
            self.logger.error("Connection refused. Ensure the server is running.")
            print("Connection refused. Ensure the server is running.")
        except Exception as e:
            # Handle other connection errors
            self.logger.error(f"An error occurred while connecting to the server: {e}")
            print(f"An error occurred while connecting to the server: {e}")
            
    def action(self):
        self.command = "null"
        action = input("\nenter your action (upload/download): ")
        self.client_socket.send(action.encode())
        
        if action == "upload":
            
            self.file_name = input("\n  enter the file name you want to upload (example.txt): ")
            file_name = self.file_name
            self.client_socket.send(file_name.encode())

            self.send_file(file_name)
        elif action == "download":
            
            file_to_recive = input("\n  enter the file name you want to download (example.txt): ")
            file_name = input("\n  enter a file name to save the data (example.txt): ")
            
            self.client_socket.send(file_to_recive.encode())
            
            self.receive_file(file_name)
        else:
            self.command = "break"

    def send_file(self, file_name):
        
        """
            Purpose: Transmits a file to the server.

            Parameters:
                * file_name (str): The path to the file to be sent.

            Actions:
                * Opens the file in binary read mode.
                * Reads the file contents and sends them to the server using the socket.
        """


        try:
            # Check if the file exists
            with open(f'{self.CLIENT_FILES_PATH}\\{file_name}', 'rb') as file:
                # Read the entire file content into a byte string
                data = file.read()
                # Send the file data to the server
                self.client_socket.sendall(data)
                
                # console
                print(f"\n    File '{file_name}' sent successfully from client.")
                
                # client logger file
                self.logger.info(f"File '{file_name}' sent successfully.")
        except FileNotFoundError:
            # Handle file not found error
            self.logger.error(f"Error: File '{file_name}' not found.")
            print(f"Error: File '{file_name}' not found.")
        except Exception as e:
            # Handle other file sending errors
            self.logger.error(f"An error occurred during file sending: {e}")
            print(f"An error occurred during file sending: {e}")
    

    def receive_file(self, file_name):
        
        """
            Purpose: Receives a file from the server and saves it.

            Parameters:
                * file_name (str): The desired name for the saved file.

            Actions:
                * Opens a new file in binary write mode.
                * Receives data from the server in chunks and writes them to the file.
        """

        try:      

            # Open a new file in binary write mode
            with open(f'{self.CLIENT_FILES_PATH}\\{file_name}', "wb") as file:
                # Receive data from the server in BUFFER_SIZE-byte chunk
                data = self.client_socket.recv(self.BUFFER_SIZE)
                    
                # Write chunk to the file
                file.write(data)
            
            # console
            print(f"\n    File '{file_name}' received successfully to Client.")
            
            # client logger file
            self.logger.info(f"File '{file_name}' received successfully.")
        except Exception as e:
            # Handle file receiving errors
            self.logger.error(f"An error occurred during file receiving: {e}")
            print(f"An error occurred during file receiving: {e}")

    def close_connection(self):
        
        '''
            Purpose: Terminates the connection with the server.
        
            Parameters: none
        
            Actions:
                * Closes the socket, ending the communication channel.
        '''

        try:
            # Close the socket, ending the communication channel
            if self.client_socket:
                self.client_socket.close()
            
            Client.counter += 1
            
            if  Client.counter < 3:     # for learning purpose the server cant take more than 3 clients
                # Connect to the server
                client.connect_to_server('127.0.0.1', 1234)
    
                while True:
                    # Send and receive files
                    client.action()
                    if client.command == "break":
                        client.close_connection()
                        break
            self.client_socket.close()
            # Connection closed successfully
            self.logger.info("Connection closed.")
        except OSError as e:
            self.logger.error(f"An error occurred while closing the connection: {e}")
            print(f"An error occurred while closing the client connection: {e}")

if __name__ == "__main__":        
    # Example usage:
    client = Client()
    # Connect to the server
    client.connect_to_server('127.0.0.1', 1234)
    
    while True:
        # Send and receive files
        client.action()
        if client.command == "break":
            client.close_connection()
            print("client connection closed.")
            break
