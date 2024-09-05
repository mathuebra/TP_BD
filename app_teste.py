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
    user = db.verify_login("mathuebra@gmail.com", "123e456") # TODO: mudar para verify_login(email, senha)
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

    lista = []

    if 'user_id' in session:
        user_id = session['user_id']  
        user_name = db.get_user_name(user_id)
        user_sent = db.get_conversas_sent(user_id)
        user_received = db.get_conversas_received(user_id)

        lista = []


    # Exemplo de retorno
    # [(1, 3, 'Mateus', 'to nao tchola', '02/09/2024 13:58:12'), (1, 2, 'Letícia', 'Oi letícia, tudo bem?', '29/08/2024 14:30:00'), (1, 2, 'Letícia', 'que bom então, tb estou bem', '30/08/2024 08:50:21')]
    # (3, 1, 'Mateus', 'eae gay, ta fazendo circuitos?', '02/09/2024 13:45:12')
    # Matheus



        # mensagens = []

        # for mensagem in user_sent:
        #     id_user_destino = mensagem[1]
        #     nome_destino = mensagem[2]
        #     conteudo = mensagem[3]
        #     data_envio = mensagem[4]
        #     mensagens[nome_destino].append((id_user_destino, conteudo, data_envio))
        
        # # Obtém as mensagens recebidas
        # recebidas = self.get_conversas_received(user_id)
        # for mensagem in recebidas:
        #     id_user_origem = mensagem[0]
        #     nome_origem = mensagem[2]
        #     conteudo = mensagem[3]
        #     data_envio = mensagem[4]
        #     mensagens[nome_origem].append((id_user_origem, conteudo, data_envio))

                



        return render_template('home.html', conversas=conversas)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)