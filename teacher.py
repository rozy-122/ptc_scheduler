from datetime import datetime
import pandas as pd

class Teacher():
    def __init__(self,
                 name: str,
                 classes: list,
                 start_date: datetime,
                 meeting_duration: int,
                 start_time: datetime,
                 end_time: datetime):
        self.df_schedule = pd.DataFrame()
        self.name = name
        self.classes = classes
        self.meeting_duration = meeting_duration
        self.daily_start_time = start_time
        self.daily_end_time = end_time
        self.create_schedule(start_date)

    def create_schedule(self, schedule_date: datetime):
        '''
        Generates Teacher's shedule for a given date
        :param schedule_date: date for the new shedule
        :return: self.df_schedule is modified
        '''
        start_t = datetime.combine(schedule_date.date(), self.daily_start_time.time())
        end_t = datetime.combine(schedule_date.date(), self.daily_end_time.time())

        df_new_schedule = pd.DataFrame()
        df_new_schedule["Meeting Date"] = pd.date_range(start=start_t, end=end_t, freq=f'{self.meeting_duration}min')
        df_new_schedule.set_index("Meeting Date", inplace=True)
        df_new_schedule["Student Name"] = df_new_schedule.fillna('', axis='columns', inplace=True)
        try:
            self.df_schedule = self.df_schedule.append(df_new_schedule, verify_integrity=True)
            #   verify_integritybool, default False
            #           If True, raise ValueError on creating index with duplicates.
            self.df_schedule.sort_index(inplace=True)
        except ValueError:
            pass

    def book_time(self, date_time : datetime, student_name : str):
        try:
            student = self.df_schedule.at[date_time, "Student Name"]
        except KeyError:
            self.create_schedule(date_time)
            student = self.df_schedule.at[date_time, "Student Name"]

        if student == None:
            self.df_schedule.at[date_time, "Student Name"] = student_name
            return True
        else:
            return False


'''
dtd = datetime.strptime("29/11/20", '%d/%m/%y')
stsrt = datetime.strptime("14:00", '%H:%M')
endt = datetime.strptime("18:00", '%H:%M')
teacher1 = Teacher("Ivan Ivanov", ["7a", "7b"], dtd, 10, stsrt, endt)
dtd = datetime.strptime("29/11/20", '%d/%m/%y')
teacher1.create_schedule(dtd)
dtd = datetime.strptime("27/11/20", '%d/%m/%y')
teacher1.create_schedule(dtd)

dtd = datetime.strptime("26/11/20", '%d/%m/%y')
teacher1.book_time(datetime.combine(dtd.date(), stsrt.time()),'Stud1')


print(teacher1.df_schedule)
'''