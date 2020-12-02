from datetime import datetime, timedelta
import pandas as pd

from scheduler import Scheduler
from teacher import Teacher
from student import Student

class Parent(Scheduler):
    def __init__(self,
                 kids: list,
                 start_date: datetime,
                 meeting_duration: int,
                 start_time: datetime,
                 end_time: datetime
                 ):
        '''
        Конструктор на class Parent

        :param kids: списък ученици, които са роднини
        :param start_date: начална дата на срещата
        :param meeting_duration:продължителност на една среща
        :param start_time:начален час на срещите през деня
        :param end_time:краен час на срещите за деня
        '''
        self.kids = kids
        super().__init__(start_date, meeting_duration, start_time, end_time)


    def create_schedule(self, schedule_date: datetime):
        '''
        Добавя часове за срещи в self.df_schedule за подадената дата.

        :param schedule_date: датата за която трябва да бъдат изчислени часовете.
        :return: променя self.df_schedule
        '''
        super().create_schedule(schedule_date, True)

    def reservation(self, teacher: Teacher, student: Student):
        '''
        Резервира време в графика за подадените учител и ученик

        :param teacher: обект от Teacher
        :param student: обект от Student
        :return: True ако резервацията е успешна.
        '''
        reservation_completed = False
        for date_time, row in self.df_schedule.iterrows():#обхожда всеки ред от графика
            if row["Teacher Name"] == None:
                if teacher.book_time(date_time, student.name):#ако учителят потвърди резервира времето в графика
                    self.df_schedule.at[date_time, "Student Name"] = student.name
                    self.df_schedule.at[date_time, "Teacher Name"] = teacher.name
                    reservation_completed = True
                    break
        return reservation_completed

    def request_meetings(self):
        '''
        Запълва графика на всеки учител за всяко дете

        :return: променя self.df_schedule
        '''
        for student in self.kids:
            for teacher in student.teachers:
                while not self.reservation(teacher, student):
                    #ако резервацията е неуспешна създава график за следващия работен ден и пробва да резервира отново.
                    list = self.df_schedule.index.tolist()#извлича списък с времената от индекса на self.df_schedule
                    new_timestamp = list[len(list)-1]+pd.tseries.offsets.BusinessDay(1) #добавяме един работен ден към последния ден от списъка
                    last_date = datetime.combine(new_timestamp.date(), datetime.min.time())#преобразуваме timestamp в datetime
                    self.create_schedule(last_date)#създаваме празен график за новата дата.