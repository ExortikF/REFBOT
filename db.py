import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, date, referrer_id=None):
        with self.connection:
            all_id = self.cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id,)).fetchall()
            if len(all_id) == 0:
                try:
                    if referrer_id != None:
                        print("добавился юзер по рефералке")
                        return self.cursor.execute("INSERT INTO 'users' ('user_id', 'reg_date', 'referrer_id') VALUES (?, ?, ?)", (user_id, date,referrer_id,))
                    else:
                        print("Добавился юзер")
                        return self.cursor.execute("INSERT INTO 'users' ('user_id', 'reg_date') VALUES (?, ?)", (user_id, date,))
                except Exception as er:
                    print(er, "Ошибка добавления юзера в бд")

    def count_referals(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) FROM users WHERE referrer_id = ?", (user_id,)).fetchone()[0]

    def get_number_of_users_by_current_date(self, current_date, userid):
        with self.connection:
            return self.cursor.execute("SELECT COUNT(*) FROM users WHERE (reg_date, referrer_id) = (?, ?)", (current_date, userid,)).fetchone()[0]

