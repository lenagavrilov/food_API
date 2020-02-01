import flask
from flask import request, jsonify
import sql_db_connection


app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/api/v1/data/status/all', methods=['GET'])
def status_all():
    connection = sql_db_connection.db_connection()
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    status_all = cursor.execute("Select * from orders_history").fetchall()
    return jsonify(status_all)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/data/status/filter', methods=['GET'])
def status_filter():
    query_parameters = request.args
    update_time = query_parameters.get("Update_Time")
    id_user = query_parameters.get("ID_User")
    status = query_parameters.get('Status')
    additional_info = query_parameters.get('Additional_Info')

    sql_query = 'SELECT * FROM orders_history WHERE'
    to_filter = []

    if update_time:
        sql_query += ' update_time=? AND'
        to_filter.append(update_time)
    if id_user:
        sql_query += ' ID_User=? AND'
        to_filter.append(id_user)
    if status:
        sql_query += ' status=? AND'
        to_filter.append(status)
    if additional_info:
        sql_query += ' additional_info=? AND'
        to_filter.append(additional_info)
    if not (update_time or id_user or status or additional_info):
        return page_not_found(404)

    sql_query = sql_query[:-4] + ';'

    connection = sql_db_connection.db_connection()
    connection.row_factory = dict_factory
    cursor = connection.cursor()
    results = cursor.execute(sql_query, to_filter).fetchall()

    return jsonify(results)


if __name__ == '__main__':
    app.run()

