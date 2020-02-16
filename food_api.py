import flask
from flask import request, jsonify
import pyodbc

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def db_connection():
    connection = pyodbc.connect(
        'Driver={ODBC Driver 13 for SQL Server};'
        'Server=DESKTOP-7FQ889E\SQLEXPRESS;'
        'Database=Food_Log;'
        'Trusted_Connection=yes;'
    )
    return connection


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Orders history</h1>'''


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/all', methods=['GET'])
def status_all():
    connection = db_connection()
    cursor = connection.cursor()
    all_status = cursor.execute('select * from order_history').fetchall()
    columns = [column[0] for column in cursor.description]
    result = []
    [result.append(dict(zip(columns, row))) for row in all_status]
    return jsonify(result)


@app.route('/filter', methods=['GET'])
def database_filter():
    query_parameters = request.args
    id = query_parameters.get("ID_User")
    status = query_parameters.get("Status")
    update = query_parameters.get("Update_Time")
    info = query_parameters.get("Additional_Info")
    query = """Select * from order_history where"""
    to_filter = []
    if id:
        query += ' ID_User=? AND'
        to_filter.append(id)
    if status:
        query += ' Status=? AND'
        to_filter.append(status)
    if update:
        query += ' Update_Time=? AND'
        to_filter.append(update)
    if info:
        query += ' Additional_info=? AND'
        to_filter.append(info)
    if not (id or status or update or info):
        return page_not_found(404)

    query = query[:-4] + ';'

    connection = db_connection()
    cursor = connection.cursor()
    filtered_result = cursor.execute(query, to_filter).fetchall()
    columns = [column[0] for column in cursor.description]
    result = []
    [result.append(dict(zip(columns, row))) for row in filtered_result]
    print(result)
    return jsonify(result)


@app.route('/add', methods=['POST'])
def get_data():
    if not request.is_json:
        return "The input data is not in a json format."
    else:
        content = request.get_json()
        # print(content)
        data_to_write_to_db = []
        [data_to_write_to_db.append(value) for value in content.values()]

        connection = db_connection()
        cursor = connection.cursor()
        sql_query = """INSERT INTO dbo.order_history
                        (ID_User, Status, Additional_Info)
                         VALUES (?,?,?)"""
        cursor.execute(sql_query, data_to_write_to_db)
        connection.commit()
        return 'Posted successfully.'


if __name__ == "__main__":
    app.run()

