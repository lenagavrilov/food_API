import pyodbc

log_data = [4, 'delivered', 'on time']


def db_connection():
    connection = pyodbc.connect(
        'Driver={ODBC Driver 13 for SQL Server};'
        'Server=DESKTOP-7FQ889E\SQLEXPRESS;'
        'Database=Food_Log;'
        'Trusted_Connection=yes;'
    )
    return connection


def insert_into_db(connection, list):
    cursor = connection.cursor()

    sql_command = """INSERT INTO dbo.order_history
                    (ID_User, Status, Additional_Info)
                     VALUES (?,?,?)"""
    cursor.execute(sql_command, list)
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
    insert_into_db(db_connection(), log_data)
    # select_all_from_db(db_connection())
    # delete_all(db_connection())
