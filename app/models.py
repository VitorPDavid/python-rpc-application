from contextlib import contextmanager
from peewee import *

__all__ = ['Subject', 'Student', 'Grades', 'connect_to_database']

db = SqliteDatabase('grades.db')

class Subject(Model):
    name = CharField()
    code = CharField()

    class Meta:
        database = db

class Student(Model):
    name = CharField()
    registration = CharField()

    class Meta:
        database = db

class Grades(Model):
    subject = ForeignKeyField(Subject, backref='grades')
    student = ForeignKeyField(Student, backref='grades')

    class Meta:
        database = db

@contextmanager
def connect_to_database():
    db.connect()
    yield
    db.close()
