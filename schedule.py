import sqlite3
import os

dataBaseExists = os.path.isfile('schedule.db')
dbcon = sqlite3.connect('schedule.db')

with dbcon:
    cursor = dbcon.cursor()
    if dataBaseExists:
        cursor.execute("SELECT * FROM courses")
        finishProgram = cursor.fetchone() is None
        print(finishProgram)
        while not finishProgram:
            # check for all the classes if class is free
            cursor.execute("SELECT current_course_time_left FROM classrooms WHERE current_course_time_left==(?)", 0)
            availableClasses = cursor.fetchall()
            for c in availableClasses:
                print(c)
