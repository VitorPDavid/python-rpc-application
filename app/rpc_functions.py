from peewee import *
from models import Grades, connect_to_database

def get_grades(student_registration):
    if (
        not isinstance(student_registration, str)
    ):
        raise TypeError('Matricula deve ser uma string')

    grades = None
    with connect_to_database():
        try:
            grades = Grades.select().where(Grades.registration==student_registration)
        except Grades.DoesNotExist:
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
            cr = Grades.select(fn.AVG(Grades.grade)).where(Grades.registration==student_registration).scalar()
        except Grades.DoesNotExist:
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
        except Grades.DoesNotExist:
            grade = Grades.create(registration=student_registration, grade=value, subject_code=subject_code)
            grade.save()

    return True

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
        except Grades.DoesNotExist:
            grade = None
            return f'Usuario com matricula "{student_registration}" na disciplina "{subject_code}" não tem nota cadastrada.'

    return grade.grade

def _get_student_subject_grade(student_registration, subject_code):
    return Grades.get((Grades.registration==student_registration)&(Grades.subject_code==subject_code))
