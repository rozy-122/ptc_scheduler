from datetime import datetime

from scheduler import Scheduler


class Teacher(Scheduler):
    def __init__(self,
                 name: str,
                 classes: list,
                 start_date: datetime,
                 meeting_duration: int,
                 start_time: datetime,
                 end_time: datetime):
        '''
        Конструктор на class Teacher

        :param name: име на учителя
        :param classes: списък от класове на които преподава
        :param start_date: начална дата на родителските срещи
        :param meeting_duration: продължителност на една среща
        :param start_time: начален час на срещите през деня
        :param end_time: краен час на срещите за деня
        '''
        self.name = name
        self.classes = classes
        super().__init__(start_date, meeting_duration, start_time, end_time)

    def book_time(self, date_time : datetime, student_name : str):
        '''
        Запазва час на среща за определен ученик в графика на учителя.

        :param date_time: час за среща
        :param student_name: име на ученик
        :return: True - ако поисканият час е свободен и същевременно го запазва
                 False - ако поисканият час не е свободен.
        '''
        student = None
        try:
            student = self.df_schedule.at[date_time, "Student Name"]#извлича името на ученика по date_time
        except KeyError:
            # ако date_time не съществува в графика на учителя
            self.create_schedule(date_time)# създава график за несъществуващата дата

        if student == None:
            self.df_schedule.at[date_time, "Student Name"] = student_name # записва ученика в графика
            return True
        else:
            return False