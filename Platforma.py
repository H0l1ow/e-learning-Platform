from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'    # Host MySQL
app.config['MYSQL_USER'] = 'root'         # Nazwa użytkownika MySQL
app.config['MYSQL_PASSWORD'] = ''         # Hasło użytkownika MySQL
app.config['MYSQL_DB'] = 'elearning'      # Nazwa bazy danych MySQL
mysql = MySQL(app)
app.secret_key = "my testing key" 

#Odpowiedzialne za wymaganie logowania aby dostać się na strony dalsze jak strona logowania
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Musisz się najpierw zalogować')
            return redirect(url_for('login'))
    return wrap

#Po wejściu w plik wideo, kiedy dostanie informację zwrotną dodaje do użytkownia tabeli 1 jako oznaczenie obejrzenia filmiku
@app.route('/vid1', methods=['GET', 'POST'])
@login_required
def vid1():
    if request.method == 'POST':
        username = session['name']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET vid1 = TRUE WHERE username = %s", (username,))
        mysql.connection.commit()
        cur.close()

    return render_template('vid1.html')

@app.route('/vid2', methods=['GET', 'POST'])
@login_required
def vid2():
    if request.method == 'POST':
        username = session['name']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET vid2 = TRUE WHERE username = %s", (username,))
        mysql.connection.commit()
        cur.close()

    return render_template('vid2.html')

@app.route('/vid3', methods=['GET', 'POST'])
@login_required
def vid3():
    if request.method == 'POST':
        username = session['name']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET vid3 = TRUE WHERE username = %s", (username,))
        mysql.connection.commit()
        cur.close()

    return render_template('vid3.html')


#ładowanie strony z tabelą użytkowników
@app.route('/table', methods=['GET', 'POST'])
@login_required
def table():

    cur = mysql.connect.cursor()
    cur.execute("SELECT `admin`, `username`,`vid1`, `vid2`, `vid3` FROM users")
    row_headers=[x[0] for x in cur.description]
    user = cur.fetchall()
    json_data=[]
    for result in user:
        json_data.append(dict(zip(row_headers,result)))
    #return jsonify(json_data)
    cur.close()
    
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        for i in range(len(request.get_data)):
            cur.execute("DELETE FROM `users` WHERE username =%s", (request.get_data))
            mysql.connection.commit()
            cur.close()

    return render_template('table.html', user=json_data)

#strona mająca na celu przekazanie do strony logowania
@app.route('/')
def home():
    return redirect(url_for('hello'))
#strona główna użytkownika z opcją zaznaczania czy dane wideo zostało zakończone

@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
        
    cur = mysql.connect.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", (session['name'],))
    user = cur.fetchone()
    cur.close()

    if user:
        v1z = user[4]  # Assuming vid1 is at index 4 in the SELECT query result
        v2z = user[5]  # Assuming vid2 is at index 4 in the SELECT query result
        v3z = user[6]  # Assuming vid3 is at index 4 in the SELECT query result
        adm = user[1]  # Assuming admin is at index 1 in the SELECT query result

    return render_template('main.html', v1z=v1z, v2z=v2z, v3z=v3z, adm=adm)


#zajmowanie sie logowaniem
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connect.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['logged_in'] = True
            session['name'] = username
            flash('Zalogowałeś się')
            return redirect(url_for('hello'))
        else:
            error = 'Nieprawidłowe dane, spróbuj jeszcze raz.'

    return render_template('login.html', error=error, register_url=url_for('register'))


# Strona rejestracji
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Sprawdź, czy hasło i potwierdzenie hasła są zgodne
        if password != confirm_password:
            error = 'Hasło i potwierdzenie hasła nie są zgodne.'
        else:
            # Sprawdź, czy użytkownik o danej nazwie już istnieje
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM users WHERE username=%s", (username,))
            existing_user = cur.fetchone()

            if existing_user:
                error = 'Użytkownik o tej nazwie już istnieje.'
            else:
                # Zapisz nowego użytkownika do bazy danych
                cur.execute("INSERT INTO users (admin, username, password, vid1, vid2, vid3) VALUES (0, %s, %s, 0, 0, 0)", (username, password))
                mysql.connection.commit()
                cur.close()

                flash('Zarejestrowano pomyślnie. Zaloguj się.')
                return redirect(url_for('login'))

    return render_template('register.html', error=error)


#funkcja odpowiedzialna za wylogoanie, odebranie tokenu zalogowania i przeniesienie na stronę logowania
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.pop('name', None)
    flash ('Wylogowałeś się ')
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run(debug = True)
