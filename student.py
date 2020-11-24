from teacher import Teacher

class Student():
    def __init__(self, name: str, grade: str):
        self.name = name
        self.grade = grade
        self.teachers = list()

    def find_teachers(self, all_teachers: list):
        for tchr in all_teachers:    # tchr: Teacher
            for grd in tchr.classes:   # grd:str
                if grd == self.grade:
                    self.teachers.append(tchr)
                    break