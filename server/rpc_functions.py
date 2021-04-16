from peewee import *
from .models import Student, Grade, connect_to_database

def get_grades(student_registration):
    if (
        not isinstance(student_registration, str)
    ):
        raise TypeError('Matricula deve ser uma string')

    grades = None
    with connect_to_database():
        try:
            grades = Grade.select().where(Grade.registration==student_registration)
        except Grade.DoesNotExist:
            return f'Usuario com matricula "{student_registration}" não tem nota cadastrada.'

    grades_values = []
    for grade in grades:
        grades_values.append({grade.subject_code: grade.grade})

    return grades_values

def get_cr(student_registration):
    if (
        not isinstance(student_registration, str)
    ):
        raise TypeError('Matricula deve ser uma string')

    cr = None
    with connect_to_database():
        try:
            cr = Grade.select(fn.AVG(Grade.grade)).where(Grade.registration==student_registration).scalar()
        except Grade.DoesNotExist:
            return f'Usuario com matricula "{student_registration}" não tem nenhuma nota cadastrada.'

    return cr

def set_grade(student_registration, subject_code, value):
    if (
        not isinstance(student_registration, str)
        or not isinstance(subject_code, str)
    ):
        raise TypeError('Matricula e codigo de disciplina devem ser strings')
    if not isinstance(value, float):
        raise TypeError('Nota deve ser um numero real.')

    with connect_to_database():
        try:
            grade = _get_student_subject_grade(student_registration, subject_code)
            grade.grade = value
            grade.save()
        except Grade.DoesNotExist:
            grade = Grade.create(registration=student_registration, grade=value, subject_code=subject_code)
            grade.save()

    return True

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

def get_grade(student_registration, subject_code):
    if (
        not isinstance(student_registration, str)
        or not isinstance(subject_code, str)
    ):
        raise TypeError('Matricula e codigo de disciplina devem ser strings')

    grade = None
    with connect_to_database():
        try:
            grade = _get_student_subject_grade(student_registration, subject_code)
        except Grade.DoesNotExist:
            grade = None
            return f'Usuario com matricula "{student_registration}" na disciplina "{subject_code}" não tem nota cadastrada.'

    return grade.grade

def _get_student_subject_grade(student_registration, subject_code):
    return Grade.get((Grade.registration==student_registration)&(Grade.subject_code==subject_code))
