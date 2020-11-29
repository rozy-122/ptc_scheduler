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
        self.kids = kids
        self.df_schedule = pd.DataFrame()
        self.meeting_duration = meeting_duration
        self.daily_start_time = start_time
        self.daily_end_time = end_time
        self.create_schedule(start_date)
        pass

    def create_schedule(self, schedule_date: datetime):
        '''
        Generates Parent's shedule for a given date
        :param schedule_date: date for the new shedule
        :return: self.df_schedule is modified
        '''
        start_t = datetime.combine(schedule_date.date(), self.daily_start_time.time())
        end_t = datetime.combine(schedule_date.date(), self.daily_end_time.time())

        df_new_schedule = pd.DataFrame()
        df_new_schedule["Meeting Date"] = pd.date_range(start=start_t, end=end_t, freq=f'{self.meeting_duration}min')
        df_new_schedule.set_index("Meeting Date", inplace=True)
        df_new_schedule["Student Name"] = df_new_schedule.fillna('', axis='columns', inplace=True)
        df_new_schedule["Teacher Name"] = df_new_schedule["Student Name"].copy()
        try:
            self.df_schedule = self.df_schedule.append(df_new_schedule, verify_integrity=True)
            #   verify_integritybool, default False
            #           If True, raise ValueError on creating index with duplicates.
            self.df_schedule.sort_index(inplace=True)
        except ValueError:
            pass

    def reservation(self, teacher: Teacher, student: Student):
        reservation_completed = False
        for date_time, row in self.df_schedule.iterrows():
            if row["Teacher Name"] == None:
                if teacher.book_time(date_time, student.name):
                    self.df_schedule.at[date_time, "Student Name"] = student.name
                    self.df_schedule.at[date_time, "Teacher Name"] = teacher.name
                    reservation_completed = True
                    break
        return reservation_completed

    def request_meetings(self):
        for student in self.kids:
            for teacher in student.teachers:
                while not self.reservation(teacher, student):
                    list = self.df_schedule.index.tolist()
                    last_date = (list[len(list)-1]+pd.tseries.offsets.BusinessDay(1)).date() #adding one business day to the last date in the list
                    last_date = datetime.combine(last_date, datetime.min.time())#converting date to datetime
                    self.create_schedule(last_date)


'''
dtd = datetime.strptime("27/11/20", '%d/%m/%y')
stsrt = datetime.strptime("14:00", '%H:%M')
endt = datetime.strptime("18:00", '%H:%M')
parent1 = Parent(["Std1", "Std2"], dtd, 10, stsrt, endt)
dtd = datetime.strptime("27/11/20", '%d/%m/%y')
parent1.create_schedule(dtd)
dtd = datetime.strptime("27/11/20", '%d/%m/%y')
parent1.create_schedule(dtd)


print(parent1.df_schedule)
parent1.test()
#p = Parent()
'''
