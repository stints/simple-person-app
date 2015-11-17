import json

from flask import Flask, jsonify, render_template, request
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
def person():
  conn = mysql.connect()
  cursor = conn.cursor()
  if request.method == 'POST':
    return json.dumps(request.get_json())
  else:
    cursor.execute('select first_name, last_name, birthday, zipcode from person')
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    result = []
    for d in data:
      d = dict(zip(columns, d))
      result.append(d)
    return json.dumps(result, default=date_handler)

def date_handler(obj):
  return obj.isoformat() if hasattr(obj, 'isoformat') else obj
