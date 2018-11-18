from flask import Flask, render_template, request, g, session, url_for, redirect

import psycopg2 as sql
import os
import psycopg2.errorcodes
import psycopg2.extras
from pprint import pprint
from datetime import datetime

psycopg2.errorcodes.UNIQUE_VIOLATION

app = Flask(__name__, template_folder='Templates')

DATABASE_URL = os.environ['DATABASE_URL']
app.secret_key = b'_1#y2L"F4Q8z\n\xec]/'

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
    if 'user_email' not in session.keys():
        return redirect('login')
	
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
	
    return render_template('listall.html', rows=rows)


@app.route('/listgamecards')
def listgamecards():
    if 'user_email' not in session.keys():
        return redirect('login')
	
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT,GAMECARD WHERE id = pid ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
	
    return render_template('listgamecards.html', rows=rows)


@app.route('/listboardgames')
def listboardgames():
    if 'user_email' not in session.keys():
        return redirect('login')

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
    if 'user_email' not in session.keys():
        return redirect('login')
    session.pop('user_email', None)
    return redirect(url_for('login'))

@app.route('/productdetails', methods=['GET', 'POST'])
def productdetails():
    if 'user_email' not in session.keys():
        return redirect('login')

    if request.method == "POST":      
        con = connect_db()
        cur = con.cursor()
        query = "SELECT * FROM PRODUCT WHERE Name = '%s'" % (request.args.get('product_name'))
        cur.execute(query)
        con.commit()
        rows = cur.fetchall()
        query = "SELECT Id FROM CUSTOMER WHERE Email = '%s'" % (session['user_email'])
        cur.execute(query)
        con.commit()
        rows2 = cur.fetchall()
        query = "INSERT INTO REVIEW values (%s, %s, '%s', '%s')" % (rows2[0][0], rows[0][0], request.form.get('user_comment') ,datetime.now())
        cur.execute(query)
        con.commit()
        cur.close()
        con.close()
#       return redirect('productdetails')
        return redirect('listall')
    else:        
        con = connect_db()
        cur = con.cursor()
        query = "SELECT * FROM PRODUCT WHERE Name = '%s'" % (request.args.get('product_name'))
        cur.execute(query)
        con.commit()
        rows = cur.fetchall()
        print(rows)
        query = "SELECT DISTINCT C.Email AS email, R.Comment AS comment, R.Time AS time FROM REVIEW R,PRODUCT P,CUSTOMER C WHERE Pid = '%s' AND Cid=C.Id ORDER BY Time DESC" % (rows[0][0])
        cur.execute(query)
        comments = cur.fetchall()
        con.commit()
        cur.close()
        con.close() 
        return render_template("productdetails.html", rows=rows, comments=comments)
        

@app.route('/cargo')
def cargo():
    if 'user_email' not in session.keys():
        return redirect('login')
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
    if 'user_email' not in session.keys():
        return redirect('login')
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
    if 'user_email' not in session.keys():
        return redirect('login')
    con = connect_db()
    cur = con.cursor()
    query = "SELECT Id FROM CUSTOMER WHERE Email = '%s'" % (session['user_email'])
    cur.execute(query)
    rows = cur.fetchall()
    id = -1
    for row in rows:
        id = row[0]
    query = "SELECT Quantity FROM SHOPPINGLISTITEM WHERE Cid = '%s' AND Pid = '%s'" %(id, request.args.get('product_id'))
    cur.execute(query)
    rows = cur.fetchall()
    if(len(rows) > 0):
        quantity = rows[0][0] + 1
        query = "UPDATE SHOPPINGLISTITEM SET Quantity = %s WHERE Cid = '%s' AND Pid = '%s'" % (quantity, id, request.args.get('product_id'))
        cur.execute(query)
        con.commit()
    else:
        query = "INSERT INTO SHOPPINGLISTITEM values (%s, %s, 1)" % (id, request.args.get('product_id'))
        cur.execute(query)
        con.commit()
    cur.close()
    con.close()
    return redirect(request.args.get('redirect'))
	
@app.route('/payment')
def payment():
    if 'user_email' not in session.keys():
        return redirect('login')
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT P.Name AS name, P.Price As price, S.Quantity As quantity, P.Id As id FROM PRODUCT P, SHOPPINGLISTITEM S, CUSTOMER C WHERE S.Cid = C.Id AND S.Pid = P.Id AND C.Email = '%s'" % (session['user_email'])
    cur.execute(query)
    rows = cur.fetchall()
    query =  "SELECT Cid,Pid, Quantity FROM PRODUCT,SHOPPINGLISTITEM WHERE Id = Pid AND quantity <= numberofproduct AND Cid IN (SELECT Id FROM CUSTOMER WHERE Email = '%s')" % (session['user_email'])
    cur.execute(query)
    products = cur.fetchall()
    if(len(products) != len(rows)):
        query = "DELETE FROM SHOPPINGLISTITEM WHERE Cid IN (SELECT Id FROM CUSTOMER WHERE Email = '%s')" % (session['user_email']) 
        cur.execute(query)
        cur.close()
        con.commit()
        con.close()
        return render_template("error.html", error_message="Not enough products in stock!!")
    for p in products:
        for i in range(p[2]):
            query = "INSERT INTO BUY values (%s, %s, '%s', '%s')" % (p[0], p[1], request.args.get('cargo_name'), datetime.now())
            cur.execute(query)
        query = "UPDATE PRODUCT SET numberofproduct = numberofproduct - %s WHERE Id = %s" % (p[2], p[1])
        cur.execute(query)
    query = "DELETE FROM SHOPPINGLISTITEM WHERE Cid IN (SELECT Id FROM CUSTOMER WHERE Email = '%s')" % (session['user_email']) 
    cur.execute(query)
    cur.close()
    con.commit()
    con.close()
    return render_template("payment.html", shopping_list=rows)

@app.route('/')
def index():
    return redirect('listall')

if __name__ == '__main__':
   app.run(debug = True)

