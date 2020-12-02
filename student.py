from teacher import Teacher

class Student():
    def __init__(self, name: str, grade: str):
        '''
        Конструктор на Student

        :param name: име на ученик
        :param grade: клас на ученик
        '''
        # запазва параметрите на конструктора в атрибути на класа.
        self.name = name
        self.grade = grade
        self.teachers = list()

    def find_teachers(self, all_teachers: list):
        '''
        Открива учителите от подадения списък и ги добавя в self.teachers

        :param all_teachers: списък с всички учители (обекти от class Teacher)
        :return: променя self.teachers
        '''
        for tchr in all_teachers:    # tchr: Teacher
            for grd in tchr.classes:   # grd:str
                if grd == self.grade:
                    self.teachers.append(tchr)
                    break