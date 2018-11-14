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
    global shopping_list
    check_login()
	
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
	
    return render_template('listall.html', rows=rows, shopping_list=shopping_list)


@app.route('/listgamecards')
def listgamecards():
    check_login()
	
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT DISTINCT * FROM PRODUCT,GAMECARD WHERE id = pid ORDER BY Name "
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
	
    return render_template('listgamecards.html', rows=rows, shopping_list=shopping_list)


@app.route('/listboardgames')
def listboardgames():
    check_login()

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
    check_login()
    con = connect_db()
    cur = con.cursor()
    query =  "SELECT P.Name AS name, P.Price As price, S.Quantity As quantity, P.Id As id FROM PRODUCT P, SHOPPINGLISTITEM S, CUSTOMER C WHERE S.Cid = C.Id AND S.Pid = P.Id AND C.Email = '%s'" % (session['user_email']);
    cur.execute(query)
    rows = cur.fetchall()
    con.close()
    return render_template("cargo.html", shopping_list=rows, cargo_companies=cargo_companies)

@app.route('/drop_item')
def drop_item():
    check_login();
    con = connect_db()
    cur = con.cursor()
    query = "DELETE FROM SHOPPINGLISTITEM WHERE Cid IN (SELECT Id FROM CUSTOMER WHERE Email = '%s') AND Pid = '%s';" % (session['user_email'], request.args.get('product_id'));
    cur.execute(query)
    con.commit()
    cur.close()
    con.close()
    return redirect('cargo')

@app.route('/payment')
def payment():
    check_login()
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

    cargo_name = request.args.get('cargo_name')
    return render_template("payment.html", cargo_name=cargo_name, shopping_dict_list=shopping_dict_list)

if __name__ == '__main__':
   app.run(debug = True)

