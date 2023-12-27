import subprocess
import time

def start_server():
    print("Starting server...")
    subprocess.run(["python", "Server.py"])

def start_client():
    # add a delay to ensure the server has started before the client attempts to connect
    time.sleep(2)
    print("Starting client...")
    subprocess.run(["python", "Client.py"])

if __name__ == "__main__":
    server_process = subprocess.Popen(["python", "-c", "from test import start_server; start_server()"])
    client_process = subprocess.Popen(["python", "-c", "from test import start_client; start_client()"])

    # Wait for both processes to finish
    server_process.wait()
    client_process.wait()
