from datetime import datetime, timedelta
import pandas as pd
from teacher import Teacher
from student import Student

class Parent():
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
        #запазва параметрите на конструктора в атрибути на класа.
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.kids = kids
        self.df_schedule = pd.DataFrame()#създава dataFrame, които ще съдържа графика на родителя
        self.meeting_duration = meeting_duration
        self.daily_start_time = start_time
        self.daily_end_time = end_time
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.create_schedule(start_date)#запълва графика за първия ден с часове.


    def create_schedule(self, schedule_date: datetime):
        '''
        Добавя часове за срещи в self.df_schedule за подадената дата.

        :param schedule_date: датата за която трябва да бъдат изчислени часовете.
        :return: променя self.df_schedule
        '''
        # конструираме началото(start_t) и края (end_t) на графика за деня, като комбинираме подадената дата със атрибутите на класа self.daily_start_time.time,self.daily_end_time.time()
        # ~~~~~~~~~~~~~~~
        start_t = datetime.combine(schedule_date.date(), self.daily_start_time.time())
        end_t = datetime.combine(schedule_date.date(), self.daily_end_time.time())
        # ~~~~~~~~~~~~~~~
        df_new_schedule = pd.DataFrame()#създава локален dateFrame в който ще има празен график
        df_new_schedule["Meeting Date"] = pd.date_range(start=start_t, end=end_t, freq=f'{self.meeting_duration}min')#запълва колоната meeting date с часове през определен интервал
        df_new_schedule.set_index("Meeting Date", inplace=True)# превръща колоната Meeting Date в индекс
        df_new_schedule["Student Name"] = df_new_schedule.fillna('', axis='columns', inplace=True)#добавя колоната Student Name и запълва колоната с None
        df_new_schedule["Teacher Name"] = df_new_schedule["Student Name"].copy()#създава колоната Teacher name и копира None стойностите от Student Name
        try:
            # за да се избегне повторение на часовете за срещи се използва verify_integrity=True
            self.df_schedule = self.df_schedule.append(df_new_schedule, verify_integrity=True)
            #   verify_integritybool, default False
            #           If True, raise ValueError on creating index with duplicates.
            self.df_schedule.sort_index(inplace=True)
        except ValueError:
            # при повторение на часа - self.df_schedule не се променя
            pass

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