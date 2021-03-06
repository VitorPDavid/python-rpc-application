from os import path

from peewee import *
from .models import Grade, Student, Subject

if not path.exists('grades.db'):
    db = SqliteDatabase('grades.db')
    db.connect()
    db.create_tables([Grade, Student, Subject])
    db.close()