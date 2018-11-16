from flask import Flask, render_template, request, g, session, url_for, redirect

import psycopg2 as sql
import os
import psycopg2.errorcodes
import psycopg2.extras
from pprint import pprint

psycopg2.errorcodes.UNIQUE_VIOLATION

app = Flask(__name__, template_folder='Templates')

DATABASE_URL = os.environ['DATABASE_URL']
app.secret_key = b'_1#y2L"F4Q8z\n\xec]/'

def connect_db():
    con = sql.connect(DATABASE_URL)
    con.cursor_factory = psycopg2.extras.NamedTupleCursor
    return con

def check_login():
    if 'user_email' not in session.keys():
        return redirect('login')
		
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
    check_login()
	
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
	
    return render_template('listall.html', rows=rows)


@app.route('/listgamecards')
def listgamecards():
    check_login()
	
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT,GAMECARD WHERE id = pid ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
	
    return render_template('listgamecards.html', rows=rows)


@app.route('/listboardgames')
def listboardgames():
    check_login()

    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT,BOARDGAME WHERE id = pid ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()

    return render_template('listboardgames.html', rows=rows)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        con = connect_db()
		
        cur = con.cursor()
        query = "SELECT Email,Password,Id FROM CUSTOMER \
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
    check_login()
    session.pop('user_email', None)
    return redirect(url_for('login'))



@app.route('/cargo')
def cargo():
    check_login()
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT P.Name AS name, P.Price As price, S.Quantity As quantity, P.Id As id FROM PRODUCT P, SHOPPINGLISTITEM S, CUSTOMER C WHERE S.Cid = C.Id AND S.Pid = P.Id AND C.Email = '%s'" % (session['user_email'])
    cur.execute(query)
    rows = cur.fetchall()
 
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

    if not rows:
        cargo_companies[:] = []
    else:
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
    con.close()
    return render_template("cargo.html", shopping_list=rows, cargo_companies=cargo_companies)

@app.route('/drop_item')
def drop_item():
    check_login()
    con = connect_db()
    cur = con.cursor()
    query = "DELETE FROM SHOPPINGLISTITEM WHERE Cid IN (SELECT Id FROM CUSTOMER WHERE Email = '%s') AND Pid = '%s'" % (session['user_email'], request.args.get('product_id'))
    cur.execute(query)
    con.commit()
    cur.close()
    con.close()
    return redirect('cargo')

@app.route('/add_item')
def add_item():
    check_login()
    con = connect_db()
    cur = con.cursor()
    query = "SELECT Id FROM CUSTOMER WHERE Email = '%s'" % (session['user_email'])
    cur.execute(query)
    rows = cur.fetchall()
    id = -1
    for row in rows:
        id = row[0]
    query = "INSERT INTO SHOPPINGLISTITEM values (%s, %s, 1)" % (id, request.args.get('product_id'))
    cur.execute(query)
    con.commit()
    cur.close()
    con.close()
    return redirect(request.args.get('redirect'))
	
@app.route('/payment')
def payment():
    check_login()
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT P.Name AS name, P.Price As price, S.Quantity As quantity, P.Id As id FROM PRODUCT P, SHOPPINGLISTITEM S, CUSTOMER C WHERE S.Cid = C.Id AND S.Pid = P.Id AND C.Email = '%s'" % (session['user_email'])
    cur.execute(query)
    rows = cur.fetchall()
    query = "DELETE FROM SHOPPINGLISTITEM WHERE Cid IN (SELECT Id FROM CUSTOMER WHERE Email = '%s')" % (session['user_email']) 
    cur.execute(query)
    cur.close()
    con.commit()
    con.close()
    return render_template("payment.html", shopping_list=rows)
if __name__ == '__main__':
   app.run(debug = True)

