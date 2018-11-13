from flask import Flask, render_template, request, g, session, url_for, redirect
from jinja2 import Environment

import psycopg2 as sql
import os
import psycopg2.errorcodes
import psycopg2.extras
from pprint import pprint

psycopg2.errorcodes.UNIQUE_VIOLATION

app = Flask(__name__, template_folder='Templates')

DATABASE_URL = os.environ['DATABASE_URL']
jinja_env = Environment(extensions=['jinja2.ext.do'])
#jinja2.Export('jinja_env')
app.secret_key = b'_1#y2L"F4Q8z\n\xec]/'




shopping_list = []

def connect_db():
    con = sql.connect(DATABASE_URL)
    con.cursor_factory = psycopg2.extras.NamedTupleCursor
    return con


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


#Ana sayfa
@app.route('/listall')
def listall():
    global shopping_list
    #if 'user_email' not in session.keys():
    #   return redirect('login')

    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()


    dummy = request.args.get('empty')
    if(dummy is not None):
        print("sasasasa\nsasasasasas\n------\n")
        shopping_list = []
    return render_template('listall.html', rows=rows, shopping_list=shopping_list)


@app.route('/listgamecards')
def listgamecards():
    global shopping_list
    #if 'user_email' not in session.keys():
    #   return redirect('login')

    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT,GAMECARD WHERE id = pid ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()

    dummy = request.args.get('empty')
    if(dummy is not None):
        print("sasasasa\nsasasasasas\n------\n")
        shopping_list = []
    return render_template('listgamecards.html', rows=rows, shopping_list=shopping_list)


@app.route('/listboardgames')
def listboardgames():
    global shopping_list
    #if 'user_email' not in session.keys():
    #   return redirect('login')

    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT,BOARDGAME WHERE id = pid ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()

    dummy = request.args.get('empty')
    if(dummy is not None):
        print("sasasasa\nsasasasasas\n------\n")
        shopping_list = []
    return render_template('listboardgames.html', rows=rows, shopping_list=shopping_list)











@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        con = connect_db()

        cur = con.cursor()
        query = "SELECT Email,Password FROM CUSTOMER \
                 WHERE Email = '%s' AND Password = '%s'" % (request.form.get('user_email'), request.form.get('user_password'))
        cur.execute(query)
        rows = cur.fetchall()
        con.close()
        if(len(rows) > 0):
            session['user_email'] = request.form['user_email']
            session['user_password'] = request.form['user_password']
            return redirect('listall')
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('user_email', None)
    return redirect(url_for('login'))


cargo_companies = [
    {
        'name': 'FedEx',
    },
    {
        'name': 'MNG',
    },
    {
        'name': 'Aras',
    }
]



@app.route('/cargo')
def cargo():
    return render_template("cargo.html", shopping_list=shopping_list, cargo_companies=cargo_companies)


@app.route('/payment')
def payment():

    con = connect_db()
    cur = con.cursor()
    '''
    shopping_dict_list = []
    for item in shopping_list:
        print("item: {}\n".format(item))
        query =  'SELECT DISTINCT NAME, PRICE FROM PRODUCT,BOARDGAME WHERE id = pid AND name="{}" ORDER BY Name'.format(item)
        cur.execute(query)
        _dict = {}
        _dict['name'] = cur.fetchall()[0]
        _dict['price'] = cur.fetchall()[1]
        shopping_dict_list.append(_dict)
    con.close()
    '''
    shopping_dict_list = [
        {
            'name': 'item1',
            'price': 5
        },
        {
            'name': 'item2',
            'price': 10
        },
        {
            'name': 'item3',
            'price': 15
        }
    ]

    cargo_name = request.args.get('cargo_name')
    return render_template("payment.html", cargo_name=cargo_name, shopping_dict_list=shopping_dict_list)


if __name__ == '__main__':
   app.run(debug = True)

