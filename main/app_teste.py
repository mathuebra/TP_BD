import datetime
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

# Rota para criar um novo grupo
@app.route('/create_group', methods=['POST'])
def create_group():
    data = request.get_json()
    
    # Obtém os dados do JSON
    group_name = data.get('name')
    group_description = data.get('description', '')  # Descrição é opcional
    creator_id = data.get('creator_id')
    group_members = data.get('members', [])
    
    if not group_name or not creator_id:
        return jsonify({'error': 'Nome do grupo e criador são obrigatórios'}), 400
    
    try:
        # Cria o grupo
        group_id = db.create_group(group_name, group_description, creator_id, group_members)
        return jsonify({'group_id': group_id}), 201
    except Exception as e:
        # Em caso de erro, retorna uma mensagem de erro
        return jsonify({'error': str(e)}), 500

# Rota para adicionar um usuário a um grupo
@app.route('/add_to_group', methods=['POST'])
def add_to_group():
    if 'user_id' in session:
        user_id = session['user_id']
        group_id = request.form.get('group_id')
        new_member = request.form.get('new_member')

        if not group_id or not new_member:
            return jsonify({'status': 'error', 'message': 'Group ID and new member are required'}), 400
        
        try:
            # Adicionar o usuário ao grupo na base de dados
            db.insert("PARTICIPA_DE", ["ID_USER", "ID_GRUPO", "ADMINISTRADOR"], [new_member, group_id, False])
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

# Rota para enviar uma mensagem para um grupo
@app.route('/send_group_message', methods=['POST'])
def send_group_message():
    if 'user_id' in session:
        user_id = session['user_id']
        group_id = request.form.get('group_id')
        message = request.form.get('message')
        
        if not group_id or not message:
            return jsonify({'status': 'error', 'message': 'Group ID and message are required'}), 400
        
        try:
            # Enviar a mensagem para o grupo na base de dados
            db.insert("MENSAGEM_GRUPO", ["ID_USER", "ID_GRUPO", "CONTEUDO", "DATA_ENVIO"], [user_id, group_id, message, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
            return jsonify({'status': 'success'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    else:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401
    
@app.route('/filter', methods=['POST'])
def filter():
    if 'user_id' in session:
        user_id = session['user_id']
        


if __name__ == '__main__':
    app.run(debug=True)