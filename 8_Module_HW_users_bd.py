from datetime import date, timedelta

users = [{'name': 'Anton', 'birthday': date(2000, 1, 1)},
         {'name': 'Stela', 'birthday': date(1987, 5, 17)},
         {'name': 'Ulano', 'birthday': date(1988, 5, 25)},
         {'name': 'Nadya', 'birthday': date(1991, 6, 13)},
         {'name': 'Codya', 'birthday': date(1990, 6, 14)},
         {'name': 'Verja', 'birthday': date(1993, 8, 3)},
         {'name': 'Maksi', 'birthday': date(1992, 7, 15)},
         {'name': 'Adama', 'birthday': date(1996, 5, 11)},
         {'name': 'Leona', 'birthday': date(1999, 9, 8)},
         {'name': 'Zarya', 'birthday': date(1996, 1, 11)},
         {'name': 'Sveta', 'birthday': date(1997, 3, 19)},
         {'name': 'Varya', 'birthday': date(1993, 5, 23)},
         {'name': 'Vadim', 'birthday': date(1995, 1, 10)},
         {'name': 'Grina', 'birthday': date(1988, 4, 11)},
         {'name': 'Roman', 'birthday': date(1989, 5, 12)},
         {'name': 'Dasha', 'birthday': date(1986, 7, 14)},
         {'name': 'Katya', 'birthday': date(1999, 9, 15)},
         {'name': 'Diana', 'birthday': date(2003, 5, 9)},
         {'name': 'Anton', 'birthday': date(2001, 6, 19)},
         ]

TY = date.today().year

def get_birthdays_per_week(users):

    date_in_week = date.today()
    current_weekday = date_in_week.weekday()
    date_in_week = date_in_week + timedelta(days=7 - current_weekday) 

    print("\nTo congratulate with Birthday next week:\n")

    for _ in range(5):
        line = []  
        for user in users:
            bd = user.get("birthday").replace(year=TY)
            user_name = user.get("name")
            if date_in_week.weekday() == 0:
                if bd == date_in_week - timedelta(days=2):
                    line.append(user_name)
                if bd == date_in_week - timedelta(days=1):
                    line.append(user_name)
            if bd == date_in_week:
                line.append(user_name)

        sline = ""
        sline = ",".join(line)
        print(f"{date_in_week.strftime('%A')}: {sline}")       
        date_in_week += timedelta(days=1)
    print("\n")


def main():
    get_birthdays_per_week(users)

if __name__ == "__main__":
    main()