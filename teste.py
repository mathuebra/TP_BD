import new_backend

db = new_backend.BD()

# sqlquery = '''SELECT CONTEUDO, DATA_ENVIO FROM MENSAGEM_PRIVADA 
#             WHERE (ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR
#                 (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)
#                 GROUP BY DATA_ENVIO'''

# print(db.select("MENSAGEM_PRIVADA", ["CONTEUDO", "DATA_ENVIO"], "(ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)"))

# def verify_login(self, email, senha):
#     return self.select("USUARIO", "*", f"EMAIL = ? AND SENHA = ?", [email, senha])

# print(db.verify_login('mathuebra@gmail.com', '123e456'))

def get_conversas(self, user_id):
    conversas = []
    self.connect()
    return self.cursor.execute(f'''SELECT ID_USER_ORIGEM, ID_USER_DESTINO, CONTEUDO, DATA_ENVIO FROM MENSAGEM_PRIVADA WHERE
                                ID_USER_ORIGEM = ? OR ID_USER_DESTINO = ?
                                ORDER BY DATA_ENVIO''', [user_id, user_id]).fetchall()

def get_conversas2(self, user_id):
    self.connect()
    return self.cursor.execute(f'''SELECT M.ID_USER_ORIGEM, M.ID_USER_DESTINO, U.NOME, M.CONTEUDO, M.DATA_ENVIO
                                FROM MENSAGEM_PRIVADA M JOIN USUARIO U ON M.ID_USER_DESTINO = U.ID_USER
                                WHERE M.ID_USER_ORIGEM = ?
                                ORDER BY M.DATA_ENVIO ASC''', [user_id]).fetchall()

def get_conversas3(self, user_id):
    self.connect()
    return self.cursor.execute(f'''SELECT M.ID_USER_ORIGEM, M.ID_USER_DESTINO, U.NOME, M.CONTEUDO, M.DATA_ENVIO
                                FROM MENSAGEM_PRIVADA M JOIN USUARIO U ON M.ID_USER_ORIGEM = U.ID_USER
                                WHERE M.ID_USER_DESTINO = ? 
                                ORDER BY M.DATA_ENVIO ASC''', [user_id]).fetchall()
  
    
print(get_conversas2(db, 1))
print(get_conversas3(db, 1)[0])
print(db.select("USUARIO", ["NOME"], "ID_USER = ?", [1])[0][0])

alpha = get_conversas2(db, 1)
lista = []

for i in alpha:
    lista[alpha[i]] = alpha[i][3].append(alpha[i][4])

print(lista)


# print(db.select("MENSAGEM_PRIVADA", ["ID_USER_ORIGEM", "CONTEUDO", "DATA_ENVIO"], "(ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)"))

# db.connect()
# print(db.cursor.execute(f'''SELECT ID_USER_ORIGEM, CONTEUDO, DATA_ENVIO FROM MENSAGEM_PRIVADA WHERE (ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)''').fetchall())
# db.disconnect()