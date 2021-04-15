import sys

from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

from rpc_functions import get_grade, get_grades

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = (
        '/rpc-api',
    )

with SimpleXMLRPCServer(('localhost', 8100),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    server.register_function(get_grade, 'get_grade')
    server.register_function(get_grades, 'get_grades')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)