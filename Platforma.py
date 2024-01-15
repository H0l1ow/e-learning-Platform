
import json
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify, json
from functools import wraps
from flask_mysqldb import MySQL
#from flask_mysqldb import MySQLdb
from json2html import *
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'    # Host MySQL
app.config['MYSQL_USER'] = 'root'         # Nazwa użytkownika MySQL
app.config['MYSQL_PASSWORD'] = ''         # Hasło użytkownika MySQL
app.config['MYSQL_DB'] = 'elearning'      # Nazwa bazy danych MySQL
mysql = MySQL(app)
app.secret_key = "my testing key" #klucz nie powinien być składowany w pliku konfiguracyjnym ale dla uproszczenia jest tutaj

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
#Po wejściu w plik wideo, kiedy dostanię informację zwrotną dodaje do użytkownia tabeli 1 jako oznaczenie obejrzenia filmiku
@app.route('/vid1', methods=['GET', 'POST'])
@login_required
def vid1():
    if request.method == 'POST':
        with open("../static/users.json", "r") as wyniki:
            data = json.load(wyniki)
        for i in range(len(data)): 
            if session['name'] == data[i]["login"]:
                data[i]["vid1"] = True

        with open("static/users.json", "w") as wyniki:
            json.dump(data,wyniki)
            wyniki.close
        #return render_template('vid1.html')
    return render_template('vid1.html')

#ładowanie strony z tabelą użytkowników
@app.route('/table', methods=['GET', 'POST'])
@login_required
def table():
    with open("static/users.json") as compl:
        data = json.load(compl)
        data = json2html.convert(data)
        compl.close
    
    return render_template('table.html', **locals())

#strona mająca na celu przekazanie do strony logowania
@app.route('/')
def home():
    return redirect(url_for('hello'))
#strona główna użytkownika z opcją zaznaczania czy dane wideo zostało zakończone
@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    error = None
    with open("static/users.json") as compl:
        data = json.load(compl)
        compl.close
        for i in range(len(data)):
            if session['name'] == data[i]['login']:
                v1z= data[i]['vid1']
                adm= data[i]['admin']
                    
    return render_template('main.html', v1z = v1z, adm = adm)
    
#zajmowanie sie logowaniem
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
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

    return render_template('login.html', error=error)

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
