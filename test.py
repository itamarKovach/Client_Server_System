import subprocess
import time

def start_server():
    print("Starting server...")
    subprocess.run(["python", "Server.py"])  # Replace "server_script.py" with the actual filename of your server script

def start_client():
    # You might want to add a delay here to ensure the server has started before the client attempts to connect
    time.sleep(2)
    print("Starting client...")
    subprocess.run(["python", "Client.py"])  # Replace "client_script.py" with the actual filename of your client script

if __name__ == "__main__":
    server_process = subprocess.Popen(["python", "-c", "from test import start_server; start_server()"])
    client_process = subprocess.Popen(["python", "-c", "from test import start_client; start_client()"])

    # Wait for both processes to finish
    server_process.wait()
    client_process.wait()