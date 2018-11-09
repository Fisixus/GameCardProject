

from flask import Flask, render_template, request, g, session, url_for, redirect
import sqlite3 as sql
app = Flask(__name__, template_folder='Templates')

DATABASE = 'C:\sqlite\ProjeDB.db'
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_1#y2L"F4Q8z\n\xec]/'

def connect_db():
    return sql.connect(DATABASE)


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
   con.row_factory = sql.Row

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
   con.row_factory = sql.Row

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
   con.row_factory = sql.Row

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
        con.row_factory = sql.Row

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

if __name__ == '__main__':
   app.run(debug = True)

