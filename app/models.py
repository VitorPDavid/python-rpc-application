from contextlib import contextmanager
from peewee import *

__all__ = ['Grades', 'connect_to_database']

db = SqliteDatabase('grades.db')

class Grades(Model):
    registration = CharField()
    grade = FloatField()
    subject_code = CharField()

    class Meta:
        database = db

@contextmanager
def connect_to_database():
    print("Open DB connection")
    if not db.is_closed():
        yield db
    else:
        db.connect()
        yield db
    db.close()
    print("close DB connection")
