from contextlib import contextmanager
from peewee import *

__all__ = ['Grade', 'Student', 'connect_to_database']

db = SqliteDatabase('grades.db')

class Student(Model):
    registration = CharField(unique=True)
    name = CharField()

    class Meta:
        database = db

class Grade(Model):
    student = ForeignKeyField(Student, backref='grades')
    grade = FloatField()
    subject_code = CharField()

    class Meta:
        database = db

def create_database():
    db.connect()
    db.create_tables([Grade, Student])
    db.close()

@contextmanager
def connect_to_database():
    print("Server: Open DB connection")
    if not db.is_closed():
        yield db
    else:
        db.connect()
        yield db
    db.close()
    print("Server: close DB connection")
