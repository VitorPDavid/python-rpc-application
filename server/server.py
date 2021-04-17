import sys

from xmlrpc.server import SimpleXMLRPCRequestHandler, SimpleXMLRPCServer

from .rpc_functions import set_grade, list_student_grades, get_grade, get_cr
from .rpc_functions import set_student, list_students
from .rpc_functions import set_subject, list_subjects


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = (
        '/rpc-api',
    )

def exec_server(port):
    print(f"Server: Iniciando servidor na porta {port}.")
    with SimpleXMLRPCServer(('localhost', port), logRequests=False,
                            requestHandler=RequestHandler) as server:
        server.register_introspection_functions()

        server.register_function(set_student, 'set_student')
        server.register_function(list_students, 'list_students')

        server.register_function(set_subject, 'set_subject')
        server.register_function(list_subjects, 'list_subjects')

        server.register_function(set_grade, 'set_grade')
        server.register_function(get_grade, 'get_grade')
        server.register_function(list_student_grades, 'list_student_grades')
        server.register_function(get_cr, 'get_cr')

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer: Interrupção do teclado recebida, fechando o servidor.")
            sys.exit(0)

if __name__ == '__main__':
    port = 8100

    args = sys.argv
    if len(args) > 1:        
        port = int(args[1])

    exec_server(port)