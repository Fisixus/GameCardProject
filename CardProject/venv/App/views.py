

from flask import Flask, render_template, request, g
import sqlite3 as sql
app = Flask(__name__,template_folder='Templates')

DATABASE = 'C:\sqlite\ProjeDB.db'
def connect_db():
    return sql.connect(DATABASE)
    

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def views():
   return "Hello World!"

@app.route('/list')
def list():
   con = connect_db()
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute('SELECT * FROM CUSTOMER')
   
   rows = cur.fetchall()
   con.close()
   return render_template('list.html',rows = rows)



if __name__ == '__main__':
   app.run(debug = True)

