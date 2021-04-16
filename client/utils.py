def print_options():
    print("""
Operações disponiveis:
    1 - Listar Alunos Cadastrados.
    2 - Listar Disciplinas Cadastradas.
    3 - Adicionar Aluno.
    4 - Adicionar nota.
    5 - Listas notas de um aluno.
    6 - Verificar nota de um aluno na disciplina.
    7 - Verificar CR de um aluno.
    0 - Fechar programa
    """)

def run_command(command, server_connection):
    if command == 3:
        set_aluno(server_connection)

def set_aluno(server_connection):
    registration = input("Informa o codigo de matricula:\n")
    name = input("Informa o Nome do Aluno:\n")

    added_student = server_connection.set_student(registration, name)

    if added_student:
        print('\nAluno adicionado')
    else:
        print('\nAluno Modificado')