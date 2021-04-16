import sys
import time

from multiprocessing import Process

from server.server import exec_server
from client.client import exec_client

if __name__ == "__main__":
    port=8100
    args = sys.argv
    if len(args) > 1:        
        port = int(args[1])

    server_process = Process(target=exec_server, args=(port,), daemon=True)
    server_process.start()

    time.sleep(1)

    exec_client(port)