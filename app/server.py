import sys

from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

from rpc_functions import get_grade, get_grades, get_cr, set_grade

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = (
        '/rpc-api',
    )

with SimpleXMLRPCServer(('localhost', 8100),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    server.register_function(get_grade, 'get_grade')
    server.register_function(get_grades, 'get_grades')
    server.register_function(get_cr, 'get_cr')
    server.register_function(set_grade, 'set_grade')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        sys.exit(0)