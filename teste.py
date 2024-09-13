from main import Database

db = Database.BD()

# # sqlquery = '''SELECT CONTEUDO, DATA_ENVIO FROM MENSAGEM_PRIVADA 
# #             WHERE (ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR
# #                 (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)
# #                 GROUP BY DATA_ENVIO'''

# # print(db.select("MENSAGEM_PRIVADA", ["CONTEUDO", "DATA_ENVIO"], "(ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)"))

# # def verify_login(self, email, senha):
# #     return self.select("USUARIO", "*", f"EMAIL = ? AND SENHA = ?", [email, senha])

# # print(db.verify_login('mathuebra@gmail.com', '123e456'))

# def get_conversas(self, user_id):
#     conversas = []
#     self.connect()
#     return self.cursor.execute(f'''SELECT ID_USER_ORIGEM, ID_USER_DESTINO, CONTEUDO, DATA_ENVIO FROM MENSAGEM_PRIVADA WHERE
#                                 ID_USER_ORIGEM = ? OR ID_USER_DESTINO = ?
#                                 ORDER BY DATA_ENVIO''', [user_id, user_id]).fetchall()

# def get_conversas2(self, user_id):
#     self.connect()
#     return self.cursor.execute(f'''SELECT M.ID_USER_ORIGEM, M.ID_USER_DESTINO, U.NOME, M.CONTEUDO, M.DATA_ENVIO
#                                 FROM MENSAGEM_PRIVADA M JOIN USUARIO U ON M.ID_USER_DESTINO = U.ID_USER
#                                 WHERE M.ID_USER_ORIGEM = ?
#                                 ORDER BY M.DATA_ENVIO ASC''', [user_id]).fetchall()

# def get_conversas3(self, user_id):
#     self.connect()
#     return self.cursor.execute(f'''SELECT M.ID_USER_ORIGEM, M.ID_USER_DESTINO, U.NOME, M.CONTEUDO, M.DATA_ENVIO
#                                 FROM MENSAGEM_PRIVADA M JOIN USUARIO U ON M.ID_USER_ORIGEM = U.ID_USER
#                                 WHERE M.ID_USER_DESTINO = ? 
#                                 ORDER BY M.DATA_ENVIO ASC''', [user_id]).fetchall()
  
    
# # print(get_conversas2(db, 1))
# # print(get_conversas3(db, 1)[0])
# # print(db.select("USUARIO", ["NOME"], "ID_USER = ?", [1])[0][0])

# # print(db.verify_conversas(1, 2))
# # print(db.get_all_users())
# # print(db.get_conversas(1, 2))


# user_id = 1
# conversas_active = [] 
# conversas = []
# all_users = db.get_all_users()
        
# for user in all_users:
#     current_user = user[0]
#     if db.verify_conversas(user_id, current_user):
#         conversas_active.append(current_user)  

# for current in conversas_active:
#     user_conversas = db.get_conversas(user_id, current)
#     conversas.append({
#         'user_id': db.get_user_name(current),
#         'conversas': user_conversas
#     })

# print(conversas)

# db.create_group("Grupo 1", "Grupo de teste", 1, [1,2,3])

# print(db.select("MENSAGEM_PRIVADA", ["ID_USER_ORIGEM", "CONTEUDO", "DATA_ENVIO"], "(ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)"))

# db.connect()
# print(db.cursor.execute(f'''SELECT ID_USER_ORIGEM, CONTEUDO, DATA_ENVIO FROM MENSAGEM_PRIVADA WHERE (ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)''').fetchall())
# db.disconnect()

# print(db.filter_message_sent(1))
conversas = []
messages = db.filter_message_sent(1)
for current in messages:
    conversas.append({
        'user_name': current[2],
        'message': current[0],
        'date': current[1]
    })
    
# print(conversas)

# print(db.get_group_message(2))
# print(db.verify_all_groups(1))

# grupo_active = db.verify_all_groups(1)
# print(grupo_active)

grupo_active = []
grupo_message = []

user_id = 1

for each in db.verify_all_groups(user_id):
    grupo_active.append(each[0])
    
for current in grupo_active:
    grupo_total_conversas = db.get_group_message(current)
    qnt_msg_grupo = db.get_qnt_message_group(current)
    for actual in range(qnt_msg_grupo):
        grupo_message.append({
            'group_id': current,
            'user_name': grupo_total_conversas[actual][2],
            'message': grupo_total_conversas[actual][0],
            'date': grupo_total_conversas[actual][1]
        })
    
print(grupo_message)

# print(db.get_conversas(1, 2))
    # if 'user_id' in session:
    #     user_id = session['user_id'] # Pega o id do usuário logado
    #     all_users = db.get_all_users() # Gera o id de todos os usuários
    #     conversas_active = [] # Lista de todos os usuários com quem o usuário logado tem conversa ativa
    #     conversas = [] # Lista todas as conversas
        
    #     for user in all_users:
    #         target_user = user[0] # Pega o id da pessoa com quem o usuário logado tem conversa
    #         if db.verify_conversas(user_id, target_user): # Verifica se o usuário logado tem conversa com a pessoa
    #             conversas_active.append(target_user) # Adiciona a pessoa na lista de conversas ativas
        
    #     for current in conversas_active:
    #         user_conversas = db.get_conversas(user_id, current) # Pega a conversa do usuário logado com o outro
    #         conversas.append({ # Gera um dicionário cuja:
    #             'user_id': current, # id do usuário atual
    #             'user_name': db.get_user_name(current), # Nome do usuário com quem o usuário logado tem a conversa
    #             'conversas': user_conversas # É a conversa em si, organizada numa tupla de 2 elementos que contem mensagem e data de envio
    #         })

    #     return render_template('home.html', conversas=conversas) # Renderiza o html home passando como parâmetro as conversas do usuário
    # else:
    #     return redirect(url_for('login')) # Se o usuário não estiver logado, redireciona pra login
    