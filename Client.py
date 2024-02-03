import socket
import ssl
import time
import os

class SSLClient:
    """
        SSLClient: A client class for secure file transfer using a client-server architecture.

        Attributes:
            hostname (str): The hostname of the server.
            port (int): The port number for the server.
            ssl_context (ssl.SSLContext): The SSL context for secure communication.
            ssl_socket (socket.socket): The underlying socket object for communication.
            CLIENT_FILES_PATH (str): Path to the directory for client files.
            command (str): The current command for client action.

        Methods:
            __init__(hostname, port): Initializes a new SSLClient instance with the specified server information.
            connect(): Initiates a secure connection with the server.
            action(): Performs an action based on user input, such as uploading or downloading files.
            send_file(): Transmits a file to the server.
            receive_file(): Receives a file from the server and saves it.
            close_connection(): Terminates the secure connection with the server.
    """

    def __init__(self, hostname, port):
        """
            Initializes the SSLClient with the specified hostname and port.

            Parameters:
                - hostname (str): The hostname of the server.
                - port (int): The port number for the server.
        """
        self.hostname = hostname
        self.port = port
        self.CLIENT_FILES_PATH = "C:\\Programming\\Network\\Client_Files"
        self.command = "null"

    def connect(self):
        """
            Connects to the server using SSL/TLS.

            Establishes a secure connection with the server by creating and wrapping a socket.

            Raises:
                - ConnectionRefusedError: If the server is not running.
                - socket.gaierror: If the address or port is invalid.
                - ssl.CertificateError: If there is a certificate-related error.
                - Exception: For unexpected errors during SSL connection setup.
        """
        try:
            # Create and wrap a socket with SSL/TLS
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.ssl_socket = self.ssl_context.wrap_socket(client_socket, server_hostname=self.hostname)

            # Connect to the server
            self.ssl_socket.connect((self.hostname, self.port))
            print(f"Client: Connected to {self.hostname}:{self.port}")

        except ConnectionRefusedError:
            print("Client: Error: Connection refused. Ensure the server is running.")
            raise

        except socket.gaierror:
            print("Client: Error: Invalid address or port.")
            raise

        except ssl.CertificateError:
            print("Client: Error: Certificate error. Make sure the server certificate is valid.")
            raise

        except Exception as e:
            print(f"Client: Error: Unexpected error during SSL connection: {str(e)}")
            raise

    def action(self):
        """
            Performs an action based on user input.

            Takes user input for the action (upload/send or download/receive) and calls the appropriate method.

            Actions:
                - Uploads/Sends a file to the server.
                - Downloads/Receives a file from the server.
        """
        time.sleep(1)
        action = input("\nClient: Enter your action (upload/send or download/receive): ")

        if action[0].lower() in {'u', 's'}:
            file_name = input("Client: Enter the name of the file you want to send to the server: ")
            self.send_file(file_name, action)

        elif action[0].lower() in {'d', 'r'}:
            self.ssl_socket.send(action.encode())
            file_name = input("Client: Enter the name of the file you want to receive from server: ")
            self.receive_file(file_name)

        else:
            self.command = "break"

    def send_file(self, file_name, action):
        """
            Sends a file to the server.

            Checks if the file exists, sends the file name to the server, and transmits the file contents.

            Parameters:
                - file_name (str): The name of the file to be sent.
                - action (str): The action identifier for upload/send.

            Raises:
                - IsADirectoryError: If attempting to send a directory instead of a file.
                - FileNotFoundError: If the specified file is not found.
                - ConnectionAbortedError: If the connection is unexpectedly aborted.
                - OSError: For other unexpected errors during file sending.
        """
        try:
            # Check if the file exists
            file_path = os.path.join(self.CLIENT_FILES_PATH, file_name)
            if not os.path.isfile(file_path):
                FileNotFoundError(f"Client: Error: File '{file_name}' not found.")
            
            if os.path.isdir(file_name):
                IsADirectoryError
                

            with open(file_path, 'rb') as file:
                self.ssl_socket.send(action.encode())
                self.ssl_socket.send(file_name.encode())

                # Read and send the file data to the server
                file_data = file.read(1024)
                while file_data:
                    self.ssl_socket.sendall(file_data)
                    file_data = file.read(1024)

                if not file_data:
                    print(f"Client: {file_name} sent successfully to the server")

        except IsADirectoryError:
            print(f"Client: Error: '{file_name}' is a directory. Please specify a file.")

        except PermissionError:
            print(f"\nServer: Error: Permission denied. Unable to read '{file_name}'.")

        except FileNotFoundError as e:
            print(f"Client: Error: No such file: {file_name}")

        except ConnectionAbortedError:
            print("Client: Error: An established connection was aborted by the software in your host machine")
            raise

        except OSError as e:
            print(f"Client: Error: Unexpected error when sending a file: {str(e)}")

    def receive_file(self, file_name):
        """
            Receives a file from the server.

            Sends the file name to receive from the server and saves the received data.

            Parameters:
                - file_name (str): The name of the file to be received.

            Raises:
                - IsADirectoryError: If attempting to receive a directory instead of a file.
                - ConnectionAbortedError: If the connection is unexpectedly aborted.
                - OSError: For other unexpected errors during file receiving.
        """
        try:
            # Send the file name to receive from the server
            self.ssl_socket.send(file_name.encode())
            
            # Receive the status code from the server indicating whether the file exists or not
            status_code = self.ssl_socket.recv(1024).decode()
            
            # Check the status code received from the server
            if status_code == "400":
                # Prompt the user for a file name to save the data
                save_file_name = input("\nClient: Enter a file name to save the data: ")

                # Open a new file in binary write mode
                with open(os.path.join(self.CLIENT_FILES_PATH, save_file_name), "wb") as file:
                    file_data = self.ssl_socket.recv(1024)
                    
                    # Write the received data to the file
                    file.write(file_data)

                    print(f"Client: {save_file_name} received and saved successfully from the server")

        except IsADirectoryError:
            print("Client: Error: Cannot receive a directory. Please specify a file name to save.")

        except ConnectionAbortedError:
            print("Client: Error: An established connection was aborted by the software in your host machine")
            raise

        except OSError as e:
            print(f"Client: Error: Unexpected error when receiving a file: {str(e)}")

    def close_connection(self):
        """
        Terminates the connection with the server.

        Closes the socket, ending the communication channel.
        """
        try:
            # Close the socket, ending the communication channel
            if self.ssl_socket:
                self.ssl_socket.close()

        except OSError as e:
            print(f"Client: Error: An error occurred while closing the client connection: {e}")
            raise

if __name__ == "__main__":
    try:
        # Example usage:
        client = SSLClient('127.0.0.1', 1234)
        # Connect to the server
        client.connect()

        while client.command == "null":
            # Send and receive files
            client.action()

    except Exception as e:
        print()

    finally:
        # Close the connection in the finally block to ensure it happens
        client.close_connection()
        print("Client: Client connection closed.")