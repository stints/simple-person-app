import datetime
import json

from flask import Flask, render_template, request
from flask.ext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'sf'
app.config['MYSQL_DATABASE_PASSWORD'] = 'servicefusionapp'
app.config['MYSQL_DATABASE_DB'] = 'servicefusion'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/api/person", methods=['GET','POST'])
def gp_person():
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'POST':
        try:
            data = request.get_json()
            cursor.execute("""insert into person \
                            (first_name, last_name, birthday, zipcode) \
                            values (%s,%s,%s,%s)""",
                            (data['first_name'].strip(),
                            data['last_name'].strip(),
                            data['birthday'].strip(),
                            data['zipcode'].strip())
                          )
            try:
                conn.commit()
                result = "inserted"
                id = cursor.lastrowid
            except:
                conn.rollback()
                result = "error"
                id = -1

            conn.close()
            return json.dumps({"result":result,"id":id})
        except Exception as e:
            conn.close()
            return json.dumps({"result":"error","error":str(e)})

    else:
        cursor.execute('select id, first_name, last_name, birthday, zipcode from person')
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = []
        for d in data:
            d = dict(zip(columns, d))
            result.append(d)
        conn.close()
        return json.dumps(result, default=date_handler)

@app.route('/api/person/<int:pid>', methods=['PUT','DELETE'])
def pd_person(pid):
    conn = mysql.connect()
    cursor = conn.cursor()
    if request.method == 'DELETE':
        cursor.execute('delete from person where id = %s', str(pid))
        try:
            conn.commit()
            result = "deleted"
        except:
            conn.rollback()
            result = "error"

        conn.close()
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            cursor.execute("""update person \
                            set first_name = %s, \
                                last_name = %s, \
                                birthday = %s, \
                                zipcode = %s \
                            where id = %s""",
                            (data['first_name'].strip(),
                            data['last_name'].strip(),
                            data['birthday'].strip(),
                            data['zipcode'].strip(),
                            int(data['id'].strip()))
                          )
            try:
                conn.commit()
                result = "updated"
            except:
                conn.rollback()
                result = "error"
        except Exception as e:
            conn.close()
            result = "major error"
            return json.dumps({'error':str(e)})

            conn.close()

    return json.dumps({'result':result})


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj
