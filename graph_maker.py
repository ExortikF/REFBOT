
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import numpy as np
from db import Database

db = Database('database_ref.db')

def count_date(): #дата сейчас
    date = datetime.date.today()
    day = "0" + str(date.day) if len(str(date.day)) == 1 else str(date.day)
    month = "0" + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    return day + month + str(date.year) #date count

def get_current_date(): #01 число месяца
    date = datetime.date.today()
    day = "01"
    month = "0" + str(date.month) if len(str(date.month)) == 1 else str(date.month)
    return [day, month, str(date.year)]  # date count

global list_of_current_date
users_statistics = []
users_statistics_earlier = []
if len(users_statistics) > 31 and len(users_statistics_earlier) > 31:
    users_statistics = []
    users_statistics_earlier = []
list_of_current_date = get_current_date()
def make_list(usid):
    for i in range(1, 32):
        list_of_current_date[0] = "0" + str(i) if i <= 9 else str(i)

        temp_date = list_of_current_date[0] + list_of_current_date[1] + list_of_current_date[2]
        temp_date2 = list_of_current_date[0] + str(int(list_of_current_date[1])-1) + list_of_current_date[2]

        users_statistics_earlier.append(db.get_number_of_users_by_current_date(temp_date2, usid))
        users_statistics.append(db.get_number_of_users_by_current_date(temp_date, usid))

month_list = []
def make_list_year(usid):
    for j in range(1,13):
        list_of_current_date[1] = "0" + str(j) if j <= 9 else str(j)
        sum = 0
        for i in range(1, 32):
            list_of_current_date[0] = "0" + str(i) if i <= 9 else str(i)
            temp_date = list_of_current_date[0] + list_of_current_date[1] + list_of_current_date[2]
            users_statistics.append(db.get_number_of_users_by_current_date(temp_date, usid))
            sum += int(db.get_number_of_users_by_current_date(temp_date, usid))
        month_list.append(sum)


def make_graph_month(userid):
    make_list(userid)
    # print(len(users_statistics))
    # print(len(users_statistics_earlier))
    # print(len([str(i+1) for i in range(31)]))
    df = pd.DataFrame({'date': np.array([str(i+1) for i in range(31)]), 'users': users_statistics}) #cопостовляем циферки с юзерами
    df2 = pd.DataFrame({'date': np.array([str(i + 1) for i in range(31)]), 'users': users_statistics_earlier}) #cопостовляем циферки с юзерами

    plt.figure(figsize=(10, 4))

    plt.plot(df.date, df.users, label='Этот месяц', linewidth=1.5)
    plt.plot(df2.date, df2.users, color='red', label='Прошлый месяц', linewidth=1.5)
    plt.yticks(np.arange(int(min(df.date)), int(max(df.date)) + 1, 1.0))
    plt.yticks(np.arange(int(min(df2.date)), int(max(df2.date)) + 1, 1.0))

    plt.title('Регистрация по реферальной ссылке')
    plt.xlabel('Дни')
    plt.ylabel('Пользователи')
    plt.legend(["Этот месяц", "Прошлый месяц"], loc="center right")


    plt.savefig(fr"Temp_graphs\{userid}.jpg")

def make_graph_year(userid):
    make_list_year(userid)
    df = pd.DataFrame({'date': np.array([str(i+1) for i in range(12)]), 'users': month_list}) #cопостовляем циферки с юзерами

    plt.figure(figsize=(10, 4))

    plt.plot(df.date, df.users, label='Этот год', linewidth=1.5)
    plt.yticks(np.arange(int(min(df.date)), int(max(df.date)) + 1, 1.0))

    plt.title('Регистрация по реферальной ссылке')
    plt.xlabel('Месяцы')
    plt.ylabel('Пользователи')
    plt.legend(["Этот год"], loc="center right")


    plt.savefig(fr"Temp_graphs\{userid}.jpg")
