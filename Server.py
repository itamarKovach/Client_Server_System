import socket
import ssl
import time
import os

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
            certfile (str): Path to the SSL certificate file. Expected format: PEM.
            keyfile (str): Path to the SSL private key file. Expected format: PEM.
            SERVER_FILES_PATH (str): Path to the directory for server files.
            server_socket (socket): The server's main socket.
            ssl_socket (ssl.SSLSocket): The SSL socket for secure communication with the client.
    """

    def __init__(self, host, port):
        # Paths to SSL certificate and private key files
        self.certfile = "C:\\Programming\\Network\\Server_Files\\cert.pem"
        self.keyfile = "C:\\Programming\\Network\\Server_Files\\key.pem"
        self.SERVER_FILES_PATH = "C:\\Programming\\Network\\Server_Files"
        
        self.server_socket = self.create_server_socket(host, port)
        self.ssl_socket = None  # Initialized in client_connection

    def create_server_socket(self, host, port):
        """
            Create and configure the server socket.

            Parameters:
                host (str): The host address.
                port (int): The port number.

            Returns:
                socket: The created server socket.
        """
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(5)
            print(f"\nServer: Server listening on {host}:{port}")
            return server_socket
        
        except Exception as e:
            print(f"\nServer: Error: unexpected error during socket setup: {e}")
            raise

    def client_connection(self):
        """
            Accepts a connection from a client and initiates secure communication.

            This method runs in a loop and handles a single connection.
        """
        try:
            client_socket, client_address = self.server_socket.accept()
            self.ssl_socket = self.wrap_ssl_socket(client_socket, client_address)
            self.handle_client(client_address)
            
        finally:
            self.stop_server()

    def wrap_ssl_socket(self, client_socket, client_address):
        """
            Wrap a regular socket in an SSL socket for secure communication.

            Parameters:
                client_socket (socket): The client's socket.
                client_address (tuple): The address of the connected client.

            Returns:
                ssl.SSLSocket: The wrapped SSL socket.
        """
        try:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            
            # Load SSL certificate and private key in PEM format
            context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
            
            ssl_socket = context.wrap_socket(client_socket, server_side=True)
            return ssl_socket

        except ssl.SSLError as e:
            if "key is incorrect" in str(e):
                # Retry with a correct key if the key is incorrect
                print("\nServer: Error: SSL Error: Key is incorrect.")
            else:
                print("\nServer: Error: SSL Error.")
            return self.wrap_ssl_socket(client_socket, client_address)

        except Exception as e:
            print(f"Server: Error: unexpected error while wrapping SSL socket: {e}")
            print(f"\nServer: Connection from {client_address} closed")
            self.ssl_socket.close()
            raise

    def handle_client(self, client_address):
        """
            Handle the communication with a connected client.

            Parameters:
                client_address (tuple): The address of the connected client.
        """
        try:
            print(f"\nServer: Connection from {client_address}")
            self.action()

        except ssl.SSLError as e:
            print(f"\nServer: Error: SSL Error: {e}")
            raise

        except ConnectionResetError:
            # Handle unexpected client disconnect
            print(f"\nServer: Error: Connection reset by the client.")

        finally:
            print(f"\nServer: Connection from {client_address} closed")
            self.ssl_socket.close()

    def action(self):
        """
            Perform actions based on commands received from the client.
            This method runs in a loop until a break command is received.
            Expected commands: 'upload', 'send', 'download', 'retrieve', 'break'.
        """
        while True:
            action = self.ssl_socket.recv(1024).decode()
            if action[0].lower() in {'u', 's'}:
                received_file_name = self.ssl_socket.recv(1024).decode()
                self.receive_file(received_file_name) 
            
            elif action[0].lower() in {'d', 'r'}:
                sent_file_name = self.ssl_socket.recv(1024).decode()
                self.send_file(sent_file_name)
                
            else:
                break

    def receive_file(self, received_file_name):
        """
            Receive a file from the client and save it on the server.

            Parameters:
                received_file_name  (str): The name of the file to be saved.
        """
        try:
            # Check if the given path is a directory
            if os.path.isdir(received_file_name):
                print(f"\nServer: Error: '{received_file_name}' is a directory. Please specify a file.")
                return            

            file_path = f"{self.SERVER_FILES_PATH}\\{received_file_name}"
            
            with open(file_path, "wb") as file:
                file_data = self.ssl_socket.recv(1024)
                file.write(file_data)

                print(f"\nServer: {received_file_name} received and saved successfully to the server")
                    
        except FileNotFoundError:
            print(f"\nServer: Error: File '{received_file_name}' not found.")
            
        except PermissionError as pe:
            print(f"\nServer: Error: {pe.strerror}. Unable to write to '{received_file_name}'.")
            
        except Exception as e:
            print(f"\nServer: Error: Unexpected error while receiving a file: {str(e)}")

    def send_file(self, sent_file_name):
        """
            Send a file to the client.

            Parameters:
                sent_file_name (str): The name of the file to be sent.
        """
        try:
            # Check if the given path is a directory
            if os.path.isdir(sent_file_name):
                raise IsADirectoryError
            
            file_path = f"{self.SERVER_FILES_PATH}\\{sent_file_name}"
            with open(file_path, 'rb') as file:
                self.ssl_socket.send("400".encode())
                file_data = file.read(1024)
                while file_data:
                    self.ssl_socket.send(file_data)
                    file_data = file.read(1024)
                if not file_data:
                    time.sleep(6)
                    print(f"\nServer: {sent_file_name} sent successfully to the client")
                    
        except FileNotFoundError:
            print(f"\nServer: Error: File '{sent_file_name}' not found.")
            self.ssl_socket.send("200".encode())
            
        except IsADirectoryError:
            print(f"Client: Error: '{sent_file_name}' is a directory. Please specify a file.")
            self.ssl_socket.send("200".encode())

        except PermissionError:
            print(f"\nServer: Error: Permission denied. Unable to read '{sent_file_name}'.")
            self.ssl_socket.send("200".encode())
            
        except Exception as e:
            print(f"\nServer: Error: Unexpected error while sending a file: {str(e)}")
            self.ssl_socket.send("200".encode())

    def stop_server(self):
        """
            Close the server socket.
        """
        try:
            if self.ssl_socket:
                self.ssl_socket.close()
            self.server_socket = None
            print("\nServer: Server closed.")
            
        except Exception as e:
            print(f"\nServer: Error: unexpected error while closing server socket: {e}")
            raise

if __name__ == "__main__":
    try:
        server = Server('127.0.0.1', 1234)
        server.client_connection()
        
    except Exception as e:
        print()