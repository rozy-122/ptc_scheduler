from datetime import datetime
import pandas as pd

class Scheduler():
    def __init__(self,
                 start_date: datetime,
                 meeting_duration: int,
                 start_time: datetime,
                 end_time: datetime):
        '''

        :param start_date:
        :param meeting_duration:
        :param start_time:
        :param end_time:
        '''
        self.df_schedule = pd.DataFrame()  # създава dataFrame, които ще съдържа график.
        # запазва параметрите на конструктора в атрибути на класа.
        # ~~~~~~~~~~~~~~~
        self.meeting_duration = meeting_duration
        self.daily_start_time = start_time
        self.daily_end_time = end_time
        # ~~~~~~~~~~~~~~~
        self.create_schedule(start_date)  # запълва графика за първия ден с часове.

    def create_schedule(self, schedule_date: datetime, create_teachers_column = False):
        '''
        Добавя часове за срещи в self.df_schedule за подадената дата.

        :param schedule_date: датата за която трябва да бъдат изчислени часовете.
        :return: променя self.df_schedule
        '''
        # конструира началото(start_t) и края (end_t) на графика за деня, като комбинира подадената дата със атрибутите на класа self.daily_start_time.time,self.daily_end_time.time()
        # ~~~~~~~~~~~~~~~
        start_t = datetime.combine(schedule_date.date(), self.daily_start_time.time())
        end_t = datetime.combine(schedule_date.date(), self.daily_end_time.time())
        # ~~~~~~~~~~~~~~~

        df_new_schedule = pd.DataFrame()  # създава локален dateFrame в който ще има празен график.
        df_new_schedule["Meeting Date"] = pd.date_range(start=start_t, end=end_t, freq=f'{self.meeting_duration}min')  # запълва колоната meeting date с часове през определен интервал
        df_new_schedule.set_index("Meeting Date", inplace=True)  # превръща колоната Meeting Date в индекс
        df_new_schedule["Student Name"] = df_new_schedule.fillna('', axis='columns', inplace=True)  # добавя колоната Student Name и запълва колоната с None
        if create_teachers_column:
            df_new_schedule["Teacher Name"] = df_new_schedule["Student Name"].copy()  # създава колоната Teacher name и копира None стойностите от Student Name
        try:
            # за да се избегне повторение на часовете за срещи се използва verify_integrity=True
            self.df_schedule = self.df_schedule.append(df_new_schedule, verify_integrity=True)  # добавя df_new_schedule, ако часовете ги няма в self.df_schedule
            #   verify_integritybool, default False
            #           If True, raise ValueError on creating index with duplicates.
            self.df_schedule.sort_index(inplace=True)
        except ValueError:
            # при повторение на часа - self.df_schedule не се променя
            pass
