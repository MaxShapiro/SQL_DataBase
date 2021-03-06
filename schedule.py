import sqlite3
import os


def main():

    dataBaseExists = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')

    with dbcon:
        cursor = dbcon.cursor()
        if dataBaseExists:
            iteration_ctr = 0
            cursor.execute("SELECT * FROM courses")
            finishProgram = cursor.fetchone() is None


            while not finishProgram:
                cursor.execute("SELECT * FROM courses")
                finishProgram = cursor.fetchone() is None
                # if the current iteration is not 0, we update the assigned classes and delete those who finished
                if (iteration_ctr != 0):
                    # updates course length in clasroom
                    cursor.execute("SELECT * FROM classrooms")
                    classroomList = cursor.fetchall()
                    for classroom in classroomList:
                        if classroom[2] != 0:  # there is a course running on that class
                            cursor.execute("UPDATE classrooms SET current_course_time_left = (?) where id = (?)",
                                           (classroom[3] - 1, classroom[0]))
                            dbcon.commit()
                            cursor.execute("SELECT * FROM classrooms where  id = (?)", (classroom[0],))
                            classroom = cursor.fetchone()
                            if classroom[3] == 0:
                                # so there is a free class
                                cursor.execute("UPDATE classrooms SET current_course_id = 0 WHERE id = (?)",
                                               (classroom[0],))
                                dbcon.commit()
                                # delete for finish courses
                                cursor.execute("DELETE FROM courses WHERE id = (?)", (classroom[2],))
                                dbcon.commit()

                # checking if there are available classes
                cursor.execute("SELECT * FROM classrooms where current_course_time_left =(?)", (0,))
                availableClasses = cursor.fetchall()

                # if we DONT have free classes - we do nothing, just skip to print
                # if we have free classes
                assigningCourses(availableClasses, cursor, dbcon, iteration_ctr)

                iteration_ctr = printing(cursor, iteration_ctr, dbcon)



def assigningCourses(availableClasses, cursor, dbcon, iteration_ctr):
    if availableClasses.__len__() != 0:
        for c in availableClasses:
            cursor.execute("SELECT * FROM courses where class_id =(?)", (c[0],))
            available_course = cursor.fetchone()

            # if  we can occupy one class
            if not available_course is None:
                print('(', iteration_ctr, ') ', c[1], ": ", available_course[1], " is schedule to start", sep='')

                # insert the course to the available class
                cursor.execute("UPDATE classrooms SET current_course_id = (?) where id = (?)",
                               (available_course[0], c[0]))
                dbcon.commit()
                cursor.execute("UPDATE classrooms SET current_course_time_left = (?) where id = (?)",
                               (available_course[5], c[0]))
                dbcon.commit()

                # update student count in student table
                cursor.execute("SELECT * FROM students where grade =(?)", (available_course[2],))
                available_student = cursor.fetchone()
                stud_count = available_student[1]
                tmp = stud_count - available_course[3]
                cursor.execute("UPDATE students SET count = (?) where grade = (?)", (tmp, available_course[2]))
                dbcon.commit()


def printing(cursor, iteration_ctr,dbcon):
    # printing status and increasing the iterator
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

    iteration_ctr += 1

    # printing the occupied classes
    cursor.execute("SELECT * FROM classrooms")
    classroomList = cursor.fetchall()
    for classroom in classroomList:
        cursor.execute("SELECT * FROM courses WHERE id = (?)", (classroom[2],))
        course = cursor.fetchone()
        if classroom[2] != 0 and classroom[3] > 1:
            print('(', iteration_ctr, ') ', classroom[1], ": occupied by ", course[1], sep='')
        elif classroom[2] != 0 and classroom[3] == 1:
            print('(', iteration_ctr, ') ', classroom[1], ": ", course[1], " is done", sep='')
            # delete for finish courses
            cursor.execute("DELETE FROM courses WHERE id = (?)", (classroom[2],))
            dbcon.commit()

            cursor.execute("UPDATE classrooms SET current_course_time_left = (?) where id = (?)", (0, classroom[0]))

            cursor.execute("SELECT * FROM classrooms WHERE id = (?)", (classroom[0],))
            classroomL = cursor.fetchall()

            assigningCourses(classroomL, cursor, dbcon, iteration_ctr)

            cursor.execute("SELECT * FROM classrooms WHERE id = (?)", (classroom[0],))
            c = cursor.fetchone()
            if c[3] != 0:
                tmp = c[3]+1
                cursor.execute("UPDATE classrooms SET current_course_time_left =(?) where  id = (?)", (tmp, classroom[0],))
                dbcon.commit()
            else:
                cursor.execute("UPDATE classrooms SET current_course_time_left = (?) where id = (?)", (1, classroom[0],))
                dbcon.commit()

    return iteration_ctr


if __name__ == '__main__':
    main()