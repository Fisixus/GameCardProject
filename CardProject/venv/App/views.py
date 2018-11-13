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
shopping_list = [] # Alisveris listesi olusturulabilir.

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
   #if 'user_email' not in session.keys():
     #   return redirect('login')
   con = connect_db()
   
   cur = con.cursor()
   query =  "SELECT DISTINCT * FROM PRODUCT ORDER BY Name "
   cur.execute(query)

   rows = cur.fetchall()
   con.close()
   return render_template('listall.html', rows=rows, shopping_list=shopping_list)

@app.route('/listgamecards')
def listgamecards():
   #if 'user_email' not in session.keys():
     #   return redirect('login')
   con = connect_db()

   cur = con.cursor()
   query =  "SELECT DISTINCT * FROM PRODUCT,GAMECARD WHERE id = pid ORDER BY Name "
   cur.execute(query)

   rows = cur.fetchall()
   con.close()
   return render_template('listgamecards.html', rows=rows, shopping_list=shopping_list)

@app.route('/listboardgames')
def listboardgames():
   #if 'user_email' not in session.keys():
     #   return redirect('login')
   con = connect_db()

   cur = con.cursor()
   query =  "SELECT DISTINCT * FROM PRODUCT,BOARDGAME WHERE id = pid ORDER BY Name "
   cur.execute(query)

   rows = cur.fetchall()
   con.close()
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
        'Name': 'Yurtici Kargo',
        'Deliver_time': '2 Weeks',
        'Price': 50
    },
    {
        'Name': 'Osman Kargo',
        'Deliver_time': '3 Days',
        'Price': 150
    },
    {
        'Name': 'UPS Kargo',
        'Deliver_time': '1 Week',
        'Price': 100
    }
]





@app.route('/cargo')
def cargo():
    item = request.args.get('item')
    con = connect_db()
    cur = con.cursor()

    query =  "SELECT DISTINCT * FROM PRODUCT,GAMECARD WHERE id = pid AND PRODUCT.name='{}' ORDER BY Name ".format(item)

    cur.execute(query)
    item_dict = cur.fetchall()[0]
    con.close()

    return render_template("cargo.html", item_dict=item_dict, cargo_companies=cargo_companies, shopping_list=shopping_list)


@app.route('/payment')
def payment():
    pprint(shopping_list)
    #cargo = request.args.get('cargo')

    for company in cargo_companies:
        if company['Name'] == cargo:
            cargo_price = company['Price']

    #total_price = float(item_price) + cargo_price
    return render_template("payment.html", shopping_list=shopping_list)
    # payment.html'ye kart mi kutu mu bilgisi goturulup 'yugioh kartiniz', 'monopoly kutu oyununuz' gibi ifadeler kullanilabilir.


if __name__ == '__main__':
   app.run(debug = True)

