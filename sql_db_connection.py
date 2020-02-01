import sqlite3


def db_connection():
    connection = sqlite3.connect('orders_history.db')
    return connection


def insert_into_db(connection, test_list):
    cursor = connection.cursor()
    print (list)
    values_to_include = [None]
    [values_to_include.append(each) for each in test_list]
    sql_command = """INSERT INTO orders_history VALUES (?,?,?,?,?);"""
    cursor.execute(sql_command, values_to_include)
    connection.commit()


def select_all_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("Select * from orders_history")
    for row in cursor:
        print(row)

def delete_all(connection):
    cursor = connection.cursor()
    cursor.execute("Delete from orders_history")
    connection.commit()


if __name__ == '__main__':
    insert_into_db(db_connection(), list)
    select_all_from_db(db_connection())
    #delete_all(db_connection())





