import os

from teacher import Teacher
from parent import Parent
#os.chdir("data")

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
            result.append(Teacher(name, classes))
    return result



def load_students():
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
            result.append((student_name, student_grade))
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
                    if student[0] == child.strip(" "):
                        children_list.append(student)
                        stud_list.remove(student)
                        break
            parent = Parent(children_list)
            result.append(parent)
    for std in stud_list:
        prnt = Parent([std])
        result.append(prnt)

            #print(parent.kids)
    return result
'''
==========================================================
'''

teachers_list = load_teachers()
for tchr in teachers_list:
    print(tchr.name, tchr.classes)

students_list = load_students()
print(students_list)

parents_list = load_parents(students_list)
for prn in parents_list:
    print(prn.kids)

#use a list comprehension to read line by line, split on ','
#and finally produce a list of tuple

#with open('t3.txt') as f:
   # mylist = [tuple(map(float, i.split(','))) for i in f]



# ifile=open("data/t2mG_00", "r")
# lines=ifile.readlines()
# data=[tuple(line.strip().split()) for line in lines]
# print(data[0])  