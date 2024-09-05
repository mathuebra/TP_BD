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
    self.connect()
    return self.cursor.execute(f'''SELECT ID_USER_ORIGEM, CONTEUDO, DATA_ENVIO FROM MENSAGEM_PRIVADA WHERE
                                (ID_USER_ORIGEM = ? AND ID_USER_DESTINO = ?) OR
                                (ID_USER_ORIGEM = ? AND ID_USER_DESTINO = ?)
                                ORDER BY DATA_ENVIO ASC''', [user_id, 2, 2, user_id]).fetchall()
    
print(get_conversas(db, 1))

print(db.verify_login('mathuebra@gmail.com', '123e456'))

# print(db.select("MENSAGEM_PRIVADA", ["ID_USER_ORIGEM", "CONTEUDO", "DATA_ENVIO"], "(ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)"))

# db.connect()
# print(db.cursor.execute(f'''SELECT ID_USER_ORIGEM, CONTEUDO, DATA_ENVIO FROM MENSAGEM_PRIVADA WHERE (ID_USER_ORIGEM = 1 AND ID_USER_DESTINO = 2) OR (ID_USER_ORIGEM = 2 AND ID_USER_DESTINO = 1)''').fetchall())
# db.disconnect()