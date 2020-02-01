from sql_db_connection import db_connection, insert_into_db, select_all_from_db

import food_api
# עד כמה לעשות בדיקות לרשימה שאני מקבלת?
# הוספתי שדה תנועהת כך שכל שורה מקבלת את המספר הייחודי

test_list = ["18/02/2020", 4, "delivered", "more info"]


def add_to_db():
    connection= db_connection()
    insert_into_db(connection, test_list)
    select_all_from_db(connection)


def start_api():
    food_api.app.run()

#add_to_db()
#start_api()