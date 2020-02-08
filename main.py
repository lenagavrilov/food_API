from database_connection import db_connection, insert_into_db
import food_api


log_data = [6, "delivered", "more info"]


def add_to_db():
    insert_into_db(db_connection(), log_data)


def start_api():
    food_api.app.run()


#add_to_db()

start_api()