from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
import Database

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'super secret key'

db = Database.BD()

# Rota para a página de login e inscrição
@app.route('/')
def login():
    return render_template('login.html')

# Rota para processar o login
@app.route('/login', methods=['POST'])
def process_login():
    email = request.form['email']
    senha = request.form['senha']
    user = db.verify_login(email, senha) # Usa o email e senha passados no html para logar
    if user:
        session['user_id'] = user[0]
        return redirect(url_for('home')) # Se o login for bem sucedido, redireciona pra home
    else:
        flash('email ou senha inválidos')
        return redirect(url_for('login')) # Se o login falhar, redireciona pra login


# Rota para processar a inscrição
@app.route('/signup', methods=['POST'])
def process_signup():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    data = request.form['data']
    db.create_user(nome, email, senha, data) # Criação de um novo usuário
    return redirect(url_for('login'))

# Rota para a página inicial que vai mostrar as conversas
@app.route('/home')
def home():
    if 'user_id' in session:
        user_id = session['user_id'] # Pega o id do usuário logado
        all_users = db.get_all_users() # Gera o id de todos os usuários
        conversas_active = [] # Lista de todos os usuários com quem o usuário logado tem conversa ativa
        conversas = [] # Lista todas as conversas
        
        for user in all_users:
            target_user = user[0] # Pega o id da pessoa com quem o usuário logado tem conversa
            if db.verify_conversas(user_id, target_user): # Verifica se o usuário logado tem conversa com a pessoa
                conversas_active.append(target_user) # Adiciona a pessoa na lista de conversas ativas
        
        for current in conversas_active:
            user_conversas = db.get_conversas(user_id, current) # Pega a conversa do usuário logado com o outro
            conversas.append({ # Gera um dicionário cuja:
                'user_id': current, # id do usuário atual
                'user_name': db.get_user_name(current), # Nome do usuário com quem o usuário logado tem a conversa
                'conversas': user_conversas # É a conversa em si, organizada numa tupla de 2 elementos que contem mensagem e data de envio
            })

        return render_template('home.html', conversas=conversas) # Renderiza o html home passando como parâmetro as conversas do usuário
    else:
        return redirect(url_for('login')) # Se o usuário não estiver logado, redireciona pra login
    
@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' in session:
        user_id = session['user_id']
        user_other = request.form['recipient_id'] # Recebe o ID do destinatário
        message = request.form['message']
        
        db.send_message(user_id, user_other, message)  # Envia a mensagem usando os IDs dos usuários

        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'User not logged in'})

if __name__ == '__main__':
    app.run(debug=True)