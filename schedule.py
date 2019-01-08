import sqlite3
import os

dataBaseExists = os.path.isfile('schedule.db')
dbcon = sqlite3.connect('schedule.db')

with dbcon:
    cursor = dbcon.cursor()
    if dataBaseExists:
        iteration_ctr = 0
        cursor.execute("SELECT * FROM courses")
        finishProgram = cursor.fetchone() is None
        while not finishProgram:
            # check for all the classes if class is free
            cursor.execute("SELECT * FROM classrooms where current_course_time_left =(?)", (0,))
            availableClasses = cursor.fetchall()
            if availableClasses is None:
                # update cuonter and course length:
                #updates course length in courses
                cursor.execute("SELECT * FROM classrooms")
                classroomList = cursor.fetchall()
                for classroom in classroomList:
                    tmp =cursor.execute("SELECT course_length FROM courses where class_id =(?)", (classroom[2],))
                    cursor.execute("UPDATE courses SET course_length = (?) where id = (?)", (tmp-1, classroom[2]))
                    # updates course length in classrooms
                    cursor.execute("UPDATE classrooms SET current_course_time_left", (classroom[3] - 1))
                    # delete finish courses
                    tmp = cursor.execute("SELECT course_length FROM courses where class_id =(?)", (classroom[2],))
                    if (tmp == 0):
                        cursor.execute("DELETE FROM courses WHERE id = (?)", (classroom[2]))
                #update counter
                iteration_ctr += 1


            else:
                for c in availableClasses:
                    cls_id = c[0]
                    cls_location = c[1]
                    cursor.execute("SELECT * FROM courses where class_id =(?)", (cls_id,))
                    available_course = cursor.fetchone()
                    crs_length = available_course[5]
                    crs_id = available_course[0]
                    if not available_course is None: # if not none we can occupy one class
                        crs_name = available_course[1]
                        print('(', iteration_ctr, ') ', cls_location, ": ", crs_name, " is scheduled to start", sep='')
                        crs_grad = available_course[2]
                        crs_num = available_course[3]
                        # update the occupied classes
                        cursor.execute("UPDATE classrooms SET current_course_id = (?) where id = (?)", (crs_id, cls_id ))
                        cursor.execute("UPDATE classrooms SET current_course_time_left = (?) where id = (?)", (crs_length, cls_id))
                        # update student count in student table
                        cursor.execute("SELECT * FROM students where grade =(?)", (crs_grad,))
                        available_student = cursor.fetchone()
                        stud_name = available_student[0]
                        stud_count = available_student[1]
                        tmp = stud_count-crs_num
                        cursor.execute("UPDATE students SET count = (?) where grade = (?)", (tmp, crs_grad))

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

                        # update the course lenght
                        cursor.execute("UPDATE courses SET course_length = (?) where id = (?)",
                                       (crs_length - 1, crs_id))
                        #update in classroom the course time left
                        cursor.execute("UPDATE classrooms SET current_course_time_left = (?) ", (c[3]-1,))

                        # delete course if the iteration time is
                        if (crs_length == 0):
                            cursor.execute("DELETE FROM courses WHERE id = (?)", (crs_id))

                        iteration_ctr += 1

                        cursor.execute("SELECT * FROM courses")
                        finishProgram = cursor.fetchone() is None

                    else:  # not succed in occipy a class
                        # update the course lenght
                        cursor.execute("UPDATE courses SET course_length = (?) where id = (?)", (crs_length-1, crs_id))

                        # update in classroom the course time left
                        cursor.execute("UPDATE classrooms SET current_course_time_left = (?) ", (c[3] - 1))

                        # delete course if the iteration time is
                        if (crs_length == 0):
                            cursor.execute("DELETE FROM courses WHERE id = (?)", (crs_id) )

                        iteration_ctr += 1

                        cursor.execute("SELECT * FROM courses")
                        finishProgram = cursor.fetchone() is None
