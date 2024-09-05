from flask import Flask, request, render_template, redirect, url_for, session, flash
import new_backend

app = Flask(__name__)
app.secret_key = 'super secret key'

db = new_backend.BD()

# Rota para a página de login e inscrição
@app.route('/')
def login():
    return render_template('login.html')

# Rota para processar o login
@app.route('/login', methods=['POST'])
def process_login():
    email = request.form['email']
    senha = request.form['senha']
    user = db.verify_login(email, senha)
    if user:
        session['user_id'] = user[0]
        return redirect(url_for('home'))
    else:
        flash('email ou senha inválidos')
        return redirect(url_for('login'))


# Rota para processar a inscrição
@app.route('/signup', methods=['POST'])
def process_signup():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    data = request.form['data']
    db.create_user(nome, email, senha, data)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id']  
        conversas = db.get_conversas(user_id) # Retorna um vetor com tuplas (ID_USER_ORIGEM, ID_USER_DESTINO, CONTEUDO, DATA_ENVIO)
        return render_template('home.html', conversas=conversas)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)