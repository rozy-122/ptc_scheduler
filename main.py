'''
Програма , която изготвя график за родителски срещи.
За вход програмата ще приема следните  файлове:
    Students – ще съдържа имената на всички ученици и техния клас.
    Teachers – ще съдържа имената на всички учители, предметите по които преподават и класовете на които преподават.
    Siblings – описва роднинските връзки между учениците.

Допълнително администраторът ще определя:
    Начална дата на срещите;
    Продължителност на срещите за един ученик;
    Време за провеждане  на срещите;

Резултатът ще бъде график за всеки учител съдържащ дати, часове и имена на ученици записани във файл,
както и график за всеки родител съдържащ дати, часове и имена на учители записани във файл.

пограмата използва pandas
pip install pandas
'''

from datetime import datetime
import loaders

#вход от потребителя: начало
input_date_time = ""
while len(input_date_time) == 0:
    input_date_time = input("Enter the start date of PTC in format 'dd/mm/yy' :")
    try:
        start_date = datetime.strptime(input_date_time, '%d/%m/%y')
    except ValueError:
        input_date_time = ""
        print("ERROR: Incorrect data format")

meeting_duration = 0
while meeting_duration < 1 or meeting_duration > 60:
    meeting_duration = int(input("Meeting duration in minutes(a number between 1 and 60): "))

input_date_time = ""
while input_date_time == "":
    input_date_time = input("Enter the start time of PTC in format 'HH:MM' :")
    try:
        start_time = datetime.strptime(input_date_time, '%H:%M')
    except ValueError:
        input_date_time = ""
        print("ERROR: Incorrect time format")

input_date_time = ""
while input_date_time == "":
    input_date_time = input("Enter the end time of PTC in format 'HH:MM' :")
    try:
        end_time = datetime.strptime(input_date_time, '%H:%M')
        if end_time <= start_time:
            input_date_time = ""
            print("ERROR: End time must be bigger than Start time")
    except ValueError:
        input_date_time = ""
        print("ERROR: Incorrect time format")
#вход от потребителя: край


teachers_list = loaders.load_teachers(start_date, meeting_duration, start_time, end_time)

students_list = loaders.load_students(teachers_list)

parents_list = loaders.load_parents(students_list, start_date, meeting_duration, start_time, end_time)

for prn in parents_list:
    prn.request_meetings()

#отпечатване на резултати
for tchr in teachers_list:
    print("="*30,f'\nTEACHER SHEDULE FOR {tchr.name}')
    tchr.df_schedule.dropna(inplace=True)
    tchr.df_schedule.to_csv(f"data/teacher_shedule_{tchr.name}.csv")
    print(tchr.df_schedule)

k = 0
for prn in parents_list:
    k += 1
    print("=" * 30, f'\nPARENT SHEDULE FOR PARENT {k}')
    prn.df_schedule.dropna(inplace=True)
    prn.df_schedule.to_csv(f"data/parent_shedule_{k}.csv")
    print(prn.df_schedule)