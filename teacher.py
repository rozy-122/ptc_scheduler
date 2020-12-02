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
        '''
        Конструктор на class Teacher

        :param name: име на учителя
        :param classes: списък от класове на които преподава
        :param start_date: начална дата на родителските срещи
        :param meeting_duration: продължителност на една среща
        :param start_time: начален час на срещите през деня
        :param end_time: краен час на срещите за деня
        '''
        self.df_schedule = pd.DataFrame() #създава dataFrame, които ще съдържа графика на учителя.
        # запазва параметрите на конструктора в атрибути на класа.
        # ~~~~~~~~~~~~~~~
        self.name = name
        self.classes = classes
        self.meeting_duration = meeting_duration
        self.daily_start_time = start_time
        self.daily_end_time = end_time
        # ~~~~~~~~~~~~~~~
        self.create_schedule(start_date) #запълва графика за първия ден с часове.

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

        df_new_schedule = pd.DataFrame() #създава локален dateFrame в който ще има празен график.
        df_new_schedule["Meeting Date"] = pd.date_range(start=start_t, end=end_t, freq=f'{self.meeting_duration}min')#запълва колоната meeting date с часове през определен интервал
        df_new_schedule.set_index("Meeting Date", inplace=True)# превръща колоната Meeting Date в индекс
        df_new_schedule["Student Name"] = df_new_schedule.fillna('', axis='columns', inplace=True)#добавя колоната Student Name и запълва колоната с None
        try:
            # за да се избегне повторение на часовете за срещи се използва verify_integrity=True
            self.df_schedule = self.df_schedule.append(df_new_schedule, verify_integrity=True)#добавя df_new_schedule, ако часовете ги няма в self.df_schedule
            #   verify_integritybool, default False
            #           If True, raise ValueError on creating index with duplicates.
            self.df_schedule.sort_index(inplace=True)
        except ValueError:
            # при повторение на часа - self.df_schedule не се променя
            pass

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