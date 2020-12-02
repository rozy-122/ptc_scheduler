from student import Student
from teacher import Teacher
from parent import Parent
from datetime import datetime

def load_teachers(_start_date: datetime,
                 _meeting_duration: int,
                 _start_time: datetime,
                 _end_time: datetime):
    '''
    Зарежда учителите от файл в списък с обекти от клас Teacher

    :param _start_date: начална дата на родителските срещи
    :param _meeting_duration: продължителност на една среща
    :param _start_time: начален час на срещите през деня
    :param _end_time: краен час на срещите за деня
    :return: списък с обекти от клас Teacher
    '''
    result = list()
    f = open("data/teachers", "r")
    header = 0#променлива за игнориране на първия ред във файла
    for line in f:
        if header == 0:
            header += 1
        else:
            line = line.strip("\n").upper()
            line_list = line.split(",", 1)#разделя реда на две части: (1)име на учител и (2)класове на които преподава
            name = line_list[0]
            classes = line_list[1].split(",")
            for i in range(len(classes)):
                classes[i] = classes[i].strip(" ")#премахва ненужните интервали в началото и в карая на сринга
            result.append(Teacher(name, classes, _start_date, _meeting_duration, _start_time, _end_time)) #създава обект и го добавя към списъка
    return result

def load_students(all_teachers: list):
    '''
    Зарежда учениците от файл в списък с обекти от клас Student

    :param all_teachers: списък от обекти Teacher
    :return: списък от обекти Student
    '''
    result = list()
    f = open("data/students", "r")
    header = 0#променлива за игнориране на първия ред във файла
    for line in f:
        if header == 0:
            header += 1
        else:
            line = line.strip("\n").upper()
            student_name, student_grade = line.split(",")
            student_name = student_name.strip(" ")
            student_grade = student_grade.strip(" ")
            stdnt = Student(student_name, student_grade)  #създава обект Student
            stdnt.find_teachers(all_teachers)
            result.append(stdnt)
    return result

def load_parents(stud_list: list,
                 _start_date: datetime,
                 _meeting_duration: int,
                 _start_time: datetime,
                 _end_time: datetime):
    '''
    Зарежда учениците с родствена връзка от файл и създава списък с обекти от клас Parent
    :param stud_list: списък с всички ученици
    :param _start_date: начална дата на родителските срещи
    :param _meeting_duration: продължителност на една среща
    :param _start_time: начален час на срещите през деня
    :param _end_time: краен час на срещите за деня
    :return: списък с обекти от клас Parent
    '''
    result = list()
    f = open("data/siblings", "r")
    header = 0#променлива за игнориране на първия ред във файла
    for line in f:
        if header == 0:
            header += 1
        else:
            line = line.strip("\n").upper()
            family = line.split(",")
            children_list = list()
            for child in family:#за всяко дете намира съответстващия обект от клас Student и го добавя към списък
                for student in stud_list:
                    if student.name == child.strip(" "):
                        children_list.append(student)
                        stud_list.remove(student)#премахва ученика от списъка, за да може в списъка да останат ученици без братя и сестри
                        break
            parent = Parent(children_list, _start_date,_meeting_duration,_start_time,_end_time)
            result.append(parent)
    for std in stud_list:#за всички ученици, които нямат братя или сестри
        prnt = Parent([std], _start_date,_meeting_duration,_start_time,_end_time)
        result.append(prnt)
    return result