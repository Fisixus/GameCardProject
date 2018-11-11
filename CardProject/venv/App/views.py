from flask import Flask, render_template, request, g, session, url_for, redirect
import psycopg2 as sql
import os
import psycopg2.errorcodes
import psycopg2.extras

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
   query =  "SELECT * FROM PRODUCT ORDER BY Name "
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
   query =  "SELECT * FROM PRODUCT,GAMECARD WHERE id = pid ORDER BY Name "
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
   query =  "SELECT * FROM PRODUCT,BOARDGAME WHERE id = pid ORDER BY Name "
   cur.execute(query)

   rows = cur.fetchall()
   con.close()
   return render_template('listboardgames.html', rows=rows)

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



item_table = [
    {
        'Name': 'Yugioh',
        'Price': 55,
        'SourceOfSupply': 'www.hepsiburada.com',
        'NumberOfProduct': 5
    },
    {
        'Name': 'Final Fantasy',
        'Price': 100,
        'SourceOfSupply': 'www.hepsiburada.com',
        'NumberOfProduct': 10
    },
    {
        'Name': 'Dj Dikkat',
        'Price': 5,
        'SourceOfSupply': 'www.mardatoni.com',
        'NumberOfProduct': 1
    },

]

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




shopping_list = {} # Alisveris listesi olusturulabilir.


@app.route('/listall_deneme')
def deneme():
    return render_template("listall_deneme.html", table=item_table)


@app.route('/cargo')
def cargo():
    item = request.args.get('item')
    for i in range (0, len(item_table)):
        if item_table[i]['Name'] == item:
            item_dict = item_table[i]

    return render_template("cargo.html", item_dict=item_dict, cargo_companies=cargo_companies)


@app.route('/payment')
def payment():
    item_name = request.args.get('item_name') # Alinan argumanlar her zaman string
    item_price = request.args.get('item_price')
    cargo = request.args.get('cargo')

    for company in cargo_companies:
        if company['Name'] == cargo:
            cargo_price = company['Price']

    total_price = int(item_price) + cargo_price
    return render_template("payment.html", item_name=item_name, total_price=total_price)
    # payment.html'ye kart mi kutu mu bilgisi goturulup 'yugioh kartiniz', 'monopoly kutu oyununuz' gibi ifadeler kullanilabilir.


if __name__ == '__main__':
   app.run(debug = True)

