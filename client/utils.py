from tabulate import tabulate

def print_options():
    print("""
Operações disponiveis:
    1 - Listar Alunos Cadastrados.
    2 - Adicionar ou modifica Aluno.
    3 - Listar Disciplinas Cadastradas.
    4 - Adicionar ou modifica Disciplina.
    5 - Listas notas de um aluno.
    6 - Adicionar ou modifica nota.
    7 - Verificar nota de um aluno na disciplina.
    8 - Verificar CR de um aluno.
    0 - Fechar programa
    """)

def run_command(command, server_connection):
    if command == 1:
        list_student(server_connection)
    elif command == 2:
        set_student(server_connection)
    elif command == 3:
        list_subjects(server_connection)
    elif command == 4:
        set_subject(server_connection)
    elif command == 5:
        list_grades(server_connection)
    elif command == 6:
        set_grade(server_connection)
    elif command == 7:
        get_grade(server_connection)
    elif command == 8:
        get_cr(server_connection)
    

def list_student(server_connection):
    students = server_connection.list_students()
    print(tabulate(students, headers=['Matricula', 'Nome']))

def set_student(server_connection):
    registration = input("Informa o codigo de matricula:\n")
    name = input("Informa o Nome do Aluno:\n")

    added_student = server_connection.set_student(registration, name)

    if added_student:
        print('\nAluno adicionado')
    else:
        print('\nAluno modificado')

def list_subjects(server_connection):
    subjects = server_connection.list_subjects()
    print(tabulate(subjects, headers=['Codigo', 'Nome']))

def set_subject(server_connection):
    code = input("Informa o codigo da Disciplina:\n")
    name = input("Informa o Nome da Disciplina:\n")

    added_subject = server_connection.set_subject(code, name)

    if added_subject:
        print('\nDisciplina adicionada')
    else:
        print('\nDisciplina modificada')

def list_grades(server_connection):
    registration = input("Informa o codigo de matricula do Aluno:\n")
    grades = server_connection.list_student_grades(registration)
    print(
        tabulate(
            grades, headers=[
                'Aluno', 'Matricula',
                'Disciplina', 'Codigo Disciplina',
                'Nota',
            ]
        )
    )

def set_grade(server_connection):
    registration = input("Informa o codigo de matricula do Aluno:\n")
    code = input("Informa o codigo da Disciplina:\n")
    grade = float(input("Informa a nota a se adicionar:\n"))

    added_grade = server_connection.set_grade(registration, code, grade)

    if added_grade:
        print('\nNota adicionada')
    else:
        print('\nNota modificada')

def get_grade(server_connection):
    registration = input("Informa o codigo de matricula do Aluno:\n")
    code = input("Informa o codigo da Disciplina:\n")

    have_grade, grade = server_connection.get_grade(registration, code)

    if have_grade:
        print(
            tabulate(
                [grade], headers=[
                    'Aluno', 'Matricula',
                    'Disciplina', 'Codigo Disciplina',
                    'Nota',
                ]
            )
        )
    else:
        print(grade)

def get_cr(server_connection):
    registration = input("Informa o codigo de matricula do Aluno:\n")

    print(f'CR do aluno: {server_connection.get_cr(registration)}')