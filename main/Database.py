import sqlite3 as sql
import os
import datetime

class BD:
    database = "/home/mathuebra/VS/TP_BD/db" # Caminho do banco de dados local
    conn = None
    cursor = None
    connected = False
    
    def connect(self):
        BD.conn = sql.connect(BD.database)
        BD.cursor = BD.conn.cursor()
        BD.connected = True
        
    def disconnect(self):
        BD.conn.close()
        BD.connected = False
        
    def execute(self, sql, parms=None):
        if BD.connected:
            if parms is None:
                BD.cursor.execute(sql)
            else:
                BD.cursor.execute(sql, parms)
            return True
        else:
            return False
        
    def fetchall(self):
        return BD.cursor.fetchall()
    
    def persist(self):
        if BD.connected:
            BD.conn.commit()
            return True
        else:
            return False
        
    def insert(self, table, columns, values):
        placeholders = ', '.join(['?'] * len(values))
        columns_str = ', '.join(columns)
        sqlquery = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

        self.connect()
        self.execute(sqlquery, values)
        self.persist()
        self.disconnect()
        
    # columns vai ser uma lista de strings e values uma lista de valores respectiva a cada column
    def update(self, table, columns, values, condition):
        place_holders = ", ".join([f"{col} = ?" for col in columns])
        sqlquery = f"UPDATE {table} SET {place_holders} WHERE {condition}"
        
        self.connect()
        self.execute(sqlquery, values)
        self.persist()
        self.disconnect()
        
    def delete(self, table, condition):
        sqlquery = f"DELETE FROM {table} WHERE {condition}"
        
        self.connect()
        self.execute(sqlquery)
        self.persist()
        self.disconnect()
        
    def select(self, table, columns, condition, params=()):
        columns = ", ".join(columns)
        sqlquery = f"SELECT {columns} FROM {table} WHERE {condition}"
        
        self.connect()
        self.execute(sqlquery, params)
        result = self.fetchall()
        self.disconnect()
        return result
        
    # Verifica se o login existe no banco de dados
    def verify_login(self, email, senha):
        result = self.select("USUARIO", ["ID_USER"], f"EMAIL = ? AND SENHA = ?", [email, senha])
        if result:
            return result[0]
    
    # Cria usuário no banco de dados
    def create_user(self, nome, email, senha, data):
        status = None
        self.insert("USUARIO", ["NOME", "STATUS", "DATA_NASCIMENTO", "EMAIL", "SENHA"], [nome, status, data, email, senha])
    
    # Retorna o nome do usuário cujo user_id é passado como parâmetro
    def get_user_name(self, user_id):
        return self.select("USUARIO", ["NOME"], "ID_USER = ?", [user_id])[0][0]
    
    def get_user_id(self, nome):
        return self.select("USUARIO", ["ID_USER"], "NOME = ?", [nome])[0][0]    
    
    # Retorna o id de todos os usuários
    def get_all_users(self):
        return self.select("USUARIO", ["ID_USER"], "1=1", [])
    
    # Retorna uma tupla de 2 elementos contendo mensagem e data de envio (formato 'DD/MM/AAAA HH:MM:SS')
    # de todas as mensagens privadas trocadas entre o usuário logado e o usuário passado como parâmetro
    def get_conversas(self, user_id, user_other):
        self.connect()
        result = self.cursor.execute(f'''SELECT CONTEUDO, DATA_ENVIO, ID_USER_ORIGEM FROM MENSAGEM_PRIVADA WHERE
                                   (ID_USER_ORIGEM = ? AND ID_USER_DESTINO = ?) OR
                                   (ID_USER_ORIGEM = ? AND ID_USER_DESTINO = ?)
                                   ORDER BY DATA_ENVIO ASC''', [user_id, user_other, user_other, user_id]).fetchall()
        self.disconnect()
        return result

    # Verifica se o usuário logado tem conversa com o usuário passado como parâmetro
    def verify_conversas(self, user_id, user_other):
        self.connect()
        result = self.cursor.execute(f'''SELECT ID_MENSAGEM FROM MENSAGEM_PRIVADA WHERE
                            ID_USER_ORIGEM = ? AND ID_USER_DESTINO = ? OR
                            ID_USER_ORIGEM = ? AND ID_USER_DESTINO = ?''', [user_id, user_other, user_other, user_id]).fetchall()
        return True if result else False
        
    def send_message(self, user_id, user_other, message):
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.insert("MENSAGEM_PRIVADA", 
                    ["ID_USER_ORIGEM", "ID_USER_DESTINO", "CONTEUDO", "DATA_ENVIO", "STATUS"], 
                    [user_id, user_other, message, current_time, "enviado"])
        
    def create_group(self, group_name, group_description, creator_id, group_members):
        self.insert("GRUPO", ["NOME_GRUPO", "DESCRICAO", "DATA_CRIACAO"], [group_name, group_description, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

        # Obtém o ID do grupo recém-criado
        self.connect()
        group_id = self.cursor.execute(f'''SELECT ID_GRUPO FROM GRUPO 
                                       ORDER BY DATA_CRIACAO DESC LIMIT 1''').fetchall()[0][0]
        self.disconnect()
        
        # Insere os membros no grupo
        for member_id in group_members:
            # Assume que o criador é um administrador por padrão
            self.insert("PARTICIPA_DE", ["ID_USER", "ID_GRUPO", "ADMINISTRADOR"], [member_id, group_id, 1 if member_id == creator_id else 0])

        return group_id