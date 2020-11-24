from student import Student
from teacher import Teacher
from parent import Parent
from datetime import datetime

def load_teachers():
    result = list()
    f = open("data/teachers", "r")
    header = 0
    for line in f:
        if header == 0:
            header += 1
        else:
            line = line.strip("\n").upper()
            line_list = line.split(",", 1)
            name = line_list[0]
            classes = line_list[1].split(",")
            for i in range(len(classes)):
                classes[i] = classes[i].strip(" ")
            result.append(Teacher(name, classes)) #list of objects (4)
    return result

def load_students(all_teachers: list):
    result = list()
    f = open("data/students", "r")
    header = 0
    for line in f:
        if header == 0:
            header += 1
        else:
            line = line.strip("\n").upper()
            student_name, student_grade = line.split(",")
            student_name = student_name.strip(" ")
            student_grade = student_grade.strip(" ")
            stdnt = Student(student_name, student_grade)  #stndt:Student
            stdnt.find_teachers(all_teachers)
            result.append(stdnt)
    return result

def load_parents(stud_list: list):
    result = list()
    f = open("data/siblings", "r")
    header = 0
    for line in f:
        if header == 0:
            header += 1
        else:
            line = line.strip("\n").upper()
            family = line.split(",")
            children_list = list()
            for child in family:
                for student in stud_list:
                    if student.name == child.strip(" "):
                        children_list.append(student)
                        stud_list.remove(student)
                        break
            parent = Parent(children_list)
            result.append(parent)
    for std in stud_list:
        prnt = Parent([std])
        result.append(prnt)
    return result
'''
==========================================START==================
'''
input_date_time = ""
while len(input_date_time) == 0:
    input_date_time = input("Enter the start date of PTC in format 'dd/mm/yy' :")
    try:
        start_date = datetime.strptime(input_date_time, '%d/%m/%y')
    except ValueError:
        input_date_time = ""
        print("ERROR: Incorrect data format")

meeting_duration = 0
while meeting_duration < 1 or meeting_duration > 60:
    meeting_duration = int(input("Meeting duration in minutes(a number between 1 and 60): "))

input_date_time = ""
while input_date_time == "":
    input_date_time = input("Enter the start time of PTC in format 'HH:MM' :")
    try:
        start_time = datetime.strptime(input_date_time, '%H:%M')
    except ValueError:
        input_date_time = ""
        print("ERROR: Incorrect time format")

input_date_time = ""
while input_date_time == "":
    input_date_time = input("Enter the end time of PTC in format 'HH:MM' :")
    try:
        end_time = datetime.strptime(input_date_time, '%H:%M')
        if end_time <= start_time:
            input_date_time = ""
            print("ERROR: End time must be bigger than Start time")
    except ValueError:
        input_date_time = ""
        print("ERROR: Incorrect time format")

teachers_list = load_teachers()
#for tchr1 in teachers_list:
    #print(tchr1.name, tchr1.classes)

students_list = load_students(teachers_list)
#for std in students_list:
    #print(std.name, std.grade)
    #for tchr2 in std.teachers:
        #print("\t", tchr2.name)

parents_list = load_parents(students_list)
n = 0
for prn in parents_list:
    n += 1
    print("="*30, "\nPARENT ", n)
    for std2 in prn.kids:
        print(std2.name, std2.grade)
        for tchr3 in std2.teachers:
            print("\t", tchr3.name)

