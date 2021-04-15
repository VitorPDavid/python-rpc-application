from peewee import *
from models import Grades, connect_to_database

def get_grades(student_registration):
    if (
        not isinstance(student_registration, str)
    ):
        raise TypeError('arg must be strings')

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

def get_grade(student_registration, subject_code):
    if (
        not isinstance(student_registration, str)
        or not isinstance(subject_code, str)
    ):
        raise TypeError('args must be strings')

    grade = None
    with connect_to_database():
        try:
            grade = Grades.get((Grades.registration==student_registration)&(Grades.subject_code==subject_code))
        except Grades.DoesNotExist:
            grade = None
            return f'Usuario com matricula "{student_registration}" na disciplina "{subject_code}" não tem nota cadastrada.'

    return grade.grade