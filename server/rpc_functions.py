from peewee import *
from .models import Student, Subject, Grade, connect_to_database

def set_student(student_registration, student_name):
    if (
        not isinstance(student_registration, str)
        or not isinstance(student_name, str)
    ):
        raise TypeError('Matricula e nome do aluno devem ser strings')

    created = True

    with connect_to_database():
        try:
            student = Student.get(Student.registration == student_registration)
            student.name = student_name
            student.save()
            created = False
        except Student.DoesNotExist:
            student = Student.create(registration=student_registration, name=student_name)
            student.save()

    return created

def get_student(student_registration):
    if (
        not isinstance(student_registration, str)
    ):
        raise TypeError('Matricula do aluno deve ser uma string')

    student = None
    with connect_to_database():
        try:
            student = Student.get(Student.registration==student_registration)
        except Student.DoesNotExist:
            student = None
            return f'Usuario com matricula "{student_registration}" não existe.'

    return student

def list_students():
    students = None
    with connect_to_database():
        students = Student.select()

    students_values = []
    for student in students:
        students_values.append(
            (student.registration, student.name)
        )

    return students_values



def set_subject(subject_code, subject_name):
    if (
        not isinstance(subject_code, str)
        or not isinstance(subject_name, str)
    ):
        raise TypeError('codigo e nome da disciplina devem ser strings')

    created = True

    with connect_to_database():
        try:
            subject = Subject.get(Subject.code == subject_code)
            subject.name = subject_name
            subject.save()
            created = False
        except Subject.DoesNotExist:
            subject = Subject.create(code=subject_code, name=subject_name)
            subject.save()

    return created

def get_subject(subject_code):
    if (
        not isinstance(subject_code, str)
    ):
        raise TypeError('Codigo da disciplina deve ser uma string')

    subject = None
    with connect_to_database():
        try:
            subject = Subject.get(Subject.code==subject_code)
        except Subject.DoesNotExist:
            subject = None
            return f'Disciplina com codigo "{subject_code}" não existe.'

    return subject

def list_subjects():
    subject = None
    with connect_to_database():
        subject = Subject.select()

    subject_values = []
    for student in subject:
        subject_values.append(
            (student.code, student.name)
        )

    return subject_values



def set_grade(student_registration, subject_code, value):
    if (
        not isinstance(student_registration, str)
        or not isinstance(subject_code, str)
    ):
        raise TypeError('Matricula e codigo de disciplina devem ser strings')
    if not isinstance(value, float):
        raise TypeError('Nota deve ser um numero real.')

    created = True

    with connect_to_database():
        try:
            grade = _get_student_subject_grade(student_registration, subject_code).get()
            grade.grade = value
            grade.save()
            created = False
        except Grade.DoesNotExist:
            student = get_student(student_registration)
            if isinstance(student, str):
                return student
            subject = get_subject(subject_code)
            if isinstance(subject, str):
                return subject

            grade = Grade.create(student=student, subject=subject, grade=value)
            grade.save()

    return created

def get_grade(student_registration, subject_code):
    if (
        not isinstance(student_registration, str)
        or not isinstance(subject_code, str)
    ):
        raise TypeError('Matricula e codigo de disciplina devem ser strings')

    with connect_to_database():
        try:
            grade = _get_student_subject_grade(student_registration, subject_code).get()
        except Grade.DoesNotExist:
            return False, f'Usuario com matricula "{student_registration}" na disciplina "{subject_code}" não tem nota cadastrada.'

    return True, (
        grade.student.name,
        grade.student.registration,
        grade.subject.name,
        grade.subject.code,
        grade.grade
    )

def list_student_grades(student_registration):
    if (
        not isinstance(student_registration, str)
    ):
        raise TypeError('Matricula deve ser uma string')

    grades = None
    with connect_to_database():
        try:
            student_model = Student.alias()
            grades = (
                Grade
                .select()
                .join(student_model, on=(Grade.student == student_model.id))
                .where(
                    student_model.registration==student_registration
                )
            )
        except Grade.DoesNotExist:
            return f'Usuario com matricula "{student_registration}" não tem nota cadastrada.'

    grades_values = []
    for grade in grades:
        grades_values.append((
            grade.student.name,
            grade.student.registration,
            grade.subject.name,
            grade.subject.code,
            grade.grade,
        ))

    return grades_values

def _get_student_subject_grade(student_registration, subject_code):
    student_model = Student.alias()
    subject_model = Subject.alias()

    return (
        Grade.select()
        .join(student_model, on=(Grade.student == student_model.id))
        .switch(Grade)
        .join(subject_model, on=(Grade.subject == subject_model.id))
        .where(
            (student_model.registration==student_registration)
            & (subject_model.code==subject_code)
        )
    )

def get_cr(student_registration):
    if (
        not isinstance(student_registration, str)
    ):
        raise TypeError('Matricula deve ser uma string')

    with connect_to_database():
        try:
            student_model = Student.alias()
            cr = (
                Grade
                .select(fn.AVG(Grade.grade))
                .join(student_model, on=(Grade.student == student_model.id))
                .where(
                    student_model.registration==student_registration
                )
            ).scalar()
        except:
            return f'Aluno com matricula "{student_registration}" não tem nenhuma nota cadastrada.'

    if cr is None:
        return f'Aluno com matricula "{student_registration}" não tem nenhuma nota cadastrada.'

    return cr