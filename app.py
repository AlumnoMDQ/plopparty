from flask import request, render_template, redirect, url_for
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from componentes.config import config

app = Flask(__name__)
app.config.from_object(config)

mysql = MySQL(app)

# app.py (continuación)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Conectar a MySQL y ejecutar la consulta
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios_ (username, email, password, is_admin, is_active) VALUES (%s, %s, %s, %s, %s)", (username, email, password, False, True))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('index'))
    
    return render_template('registro.html')
@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
