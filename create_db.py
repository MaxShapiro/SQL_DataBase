import sqlite3
import os

dataBaseExists = os.path.isfile('schedule.db')
dbcon = sqlite3.connect('schedule.db')

with dbcon:

    cursor = dbcon.cursor()
    if not dataBaseExists:
        cursor.execute("CREATE TABLE courses(id INTEGER PRIMARY KEY,"
                       " course_name TEXT NOT NULL,"
                       " student TEXT NOT NULL,"
                       " number_of_students INTEGER NOT NULL, "
                       "class_id INTEGER REFERENCES classrooms(id),"
                       " course_length INTEGER NOT NULL )")  # create table courses

        cursor.execute("CREATE TABLE students(grade TEXT PRIMARY KEY,"
                       " count INTEGER NOT NULL )")  # create table students

        cursor.execute("CREATE TABLE classrooms(id INTEGER PRIMARY KEY,"
                       " location TEXT NOT NULL,current_course_id INTEGER NOT NULL,"
                       " current_course_time_left INTEGER NOT NULL)")  # create table classrooms

with open("/home/max/Downloads/config2.txt") as f:
    ourFile = f.read()
    content = ourFile.split('\n')


for i in content:
    newList = i.split(', ')
    if newList[0] == "S":
        cursor.execute("INSERT INTO students(grade, count) VALUES(?,?)", [newList[1], newList[2]])
    elif newList[0] == "C":
        cursor.execute("INSERT INTO courses(id, course_name, student, number_of_students,"
                       " class_id, course_length) VALUES(?,?,?,?,?,?)", (newList[1], newList[2], newList[3], newList[4], newList[5], newList[6]))
    elif newList[0] == "R":
        cursor.execute("INSERT INTO classrooms(id, location, current_course_id, current_course_time_left)"
                       " VALUES(?,?,?,?)", (newList[1], newList[2], 0, 0))


cursor.execute("SELECT * FROM courses")
coursesList = cursor.fetchall()
print('courses')
for course in coursesList:
    print(str(course))

cursor.execute("SELECT * FROM classrooms")
classroomList = cursor.fetchall()
print('classrooms')
for classroom in classroomList:
    print(str(classroom))


cursor.execute("SELECT * FROM students")
studentList = cursor.fetchall()
print('students')
for student in studentList:
    print(str(student))

dbcon.commit()