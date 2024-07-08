from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config.from_object('componentes.config.Config')
app.secret_key = 'tu_clave_secreta'

# Configuración de la base de datos SQLAlchemy
db = SQLAlchemy(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Definir la clase User con UserMixin
class User(UserMixin, db.Model):
    __tablename__ = 'clientes'  # Asegúrate de que el nombre de la tabla coincida con el de tu base de datos

    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)

# Definir la función user_loader para cargar usuarios
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


mail = Mail(app)

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la página de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        nuevo_usuario = User(nombre_usuario=nombre_usuario, email=email, contraseña=contraseña)
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('registro.html')

# Ruta para la página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        
        usuario = User.query.filter_by(email=email, contraseña=contraseña).first()
        
        if usuario:
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas. Por favor, inténtalo de nuevo.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Ruta para la página de contacto
@app.route('/contacto', methods=['GET', 'POST'])
@login_required
def contacto():
    if request.method == 'POST':
        nombre = current_user.nombre_usuario
        email = current_user.email
        mensaje = request.form.get('mensaje', '')

        print(f'Debug: Nombre: {nombre}, Email: {email}, Mensaje: {mensaje}')  # Mensaje de depuración

        if not mensaje:
            flash('Por favor, ingrese un mensaje.', 'error')
            return render_template('contacto.html')

        try:
            # Enviar correo electrónico
            msg = Message('Consulta de Contacto - PlopParty',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=['ploppartytermas@gmail.com'])  # Cambiar al correo destinatario
            msg.body = f'Nombre: {nombre}\nEmail: {email}\nConsulta:\n{mensaje}'
            mail.send(msg)

            print("Correo enviado exitosamente.")  # Mensaje de depuración
            flash('Consulta enviada correctamente.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            print(f'Error al enviar el correo: {str(e)}')  # Mensaje de depuración
            flash(f'Error al enviar el correo: {str(e)}', 'error')
            return render_template('contacto.html')

    return render_template('contacto.html')



@app.route('/enviar_correo_prueba')
def enviar_correo_prueba():
    try:
        msg = Message('Correo de Prueba - PlopParty',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=['ploppartytermas@gmail.com'])  # Cambiar al correo destinatario
        msg.body = 'Este es un correo de prueba desde PlopParty.'
        mail.send(msg)

        print("Correo de prueba enviado exitosamente.")  # Mensaje de depuración
        return 'Correo de prueba enviado exitosamente.'
    except Exception as e:
        print(f'Error al enviar el correo de prueba: {str(e)}')  # Mensaje de depuración
        return f'Error al enviar el correo de prueba: {str(e)}'

# Ruta para la página de perfil del usuario
@app.route('/perfil')
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta
def perfil():
    return render_template('perfil.html', cliente=current_user)

if __name__ == '__main__':
    app.run(debug=True)
