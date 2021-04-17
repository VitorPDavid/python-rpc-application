import time
import xmlrpc.client

from .utils import print_options, run_command

def exec_client(port):
    server_connection = xmlrpc.client.ServerProxy(f'http://localhost:{port}/rpc-api')

    command = 1
    while(command != 0):
        print_options()
        try:
            command = int(input('Entre com o comando desejado:\n'))
        except:
            continue

        run_command(command, server_connection)
        time.sleep(2)

if __name__ == '__main__':
    port = 8100

    args = sys.argv
    if len(args) > 1:        
        port = int(args[1])

    exec_client(port)