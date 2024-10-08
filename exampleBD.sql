CREATE TABLE USUARIO (
    ID_USER INT PRIMARY KEY,
    NOME VARCHAR(25),
    STATUS VARCHAR(100),
    DATA_NASCIMENTO DATE,
    EMAIL VARCHAR(50) UNIQUE,
    SENHA VARCHAR(50)
);

-- Permite criação de usuários sem status, porém os outros campos são obrigatórios
CREATE OR REPLACE TRIGGER USUARIO_VAZIO
BEFORE INSERT OR UPDATE ON USUARIO FOR EACH ROW
BEGIN
    IF (:NEW.NOME IS NULL OR
        :NEW.DATA_NASCIMENTO IS NULL OR
        :NEW.EMAIL IS NULL OR
        :NEW.SENHA IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20000, 'Erro: Campos obrigatórios não preenchidos');
    END IF;
END;
/

CREATE TABLE MENSAGEM_PRIVADA (
    ID_MENSAGEM INT,
    ID_USER_ORIGEM INT,
    ID_USER_DESTINO INT,
    CONTEUDO VARCHAR(250),
    DATA_ENVIO DATE,
    STATUS VARCHAR(20),
    REACAO VARCHAR(20),
    PRIMARY KEY (ID_MENSAGEM, ID_USER_ORIGEM, ID_USER_DESTINO)
);

ALTER TABLE MENSAGEM_PRIVADA ADD CONSTRAINT FK_MENSAGEM_PRIVADA_ORIGEM FOREIGN KEY (ID_USER_ORIGEM) REFERENCES USUARIO(ID_USER);
ALTER TABLE MENSAGEM_PRIVADA ADD CONSTRAINT FK_MENSAGEM_PRIVADA_DESTINO FOREIGN KEY (ID_USER_DESTINO) REFERENCES USUARIO(ID_USER);

CREATE OR REPLACE TRIGGER MENSAGEM_PRIVADA_VAZIA
BEFORE INSERT ON MENSAGEM_PRIVADA
BEGIN
    IF (:NEW.CONTEUDO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20001, 'Erro: Mensagem vazia');
    END IF;
END;
/

CREATE TABLE MENSAGEM_GRUPO (
    ID_MENSAGEM INT,
    ID_USER_ORIGEM INT,
    ID_GRUPO_DESTINO INT,
    CONTEUDO VARCHAR(250),
    DATA_ENVIO DATE,
    PRIMARY KEY (ID_MENSAGEM, ID_USER_ORIGEM, ID_GRUPO_DESTINO)
);

ALTER TABLE MENSAGEM_GRUPO ADD CONSTRAINT FK_MENSAGEM_GRUPO_ORIGEM FOREIGN KEY (ID_USER_ORIGEM) REFERENCES USUARIO(ID_USER);
ALTER TABLE MENSAGEM_GRUPO ADD CONSTRAINT FK_MENSAGEM_GRUPO_DESTINO FOREIGN KEY (ID_GRUPO_DESTINO) REFERENCES GRUPO(ID_GRUPO);

CREATE OR REPLACE TRIGGER MENSAGEM_GRUPO_VAZIA
BEFORE INSERT ON MENSAGEM_GRUPO
BEGIN
    IF (:NEW.CONTEUDO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20001, 'Erro: Mensagem vazia');
    END IF;
END;
/

CREATE TABLE GRUPO (
    ID_GRUPO INT PRIMARY KEY,
    DESCRICAO VARCHAR(100),
    DATA_CRIACAO DATE,
    NOME_GRUPO VARCHAR(25)
);

CREATE OR REPLACE TRIGGER GRUPO_VAZIO
BEFORE INSERT ON GRUPO
BEGIN
    IF (:NEW.NOME_GRUPO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20002, 'Erro: Nome do grupo vazio');
    END IF;
END;
/

CREATE TABLE PARTICIPA_DE (
    ID_USER INT,
    ID_GRUPO INT,
    ADMINISTRADOR BOOLEAN
);

ALTER TABLE PARTICIPA_DE ADD CONSTRAINT FK_PARTICIPA_DE_USUARIO FOREIGN KEY (ID_USER) REFERENCES USUARIO(ID_USER);
ALTER TABLE PARTICIPA_DE ADD CONSTRAINT FK_PARTICIPA_DE_GRUPO FOREIGN KEY (ID_GRUPO) REFERENCES GRUPO(ID_GRUPO);

CREATE OR REPLACE TRIGGER PARTICIPA_DE_VAZIO
BEFORE INSERT ON PARTICIPA_DE
BEGIN
    IF (:NEW.ID_USER IS NULL OR
        :NEW.ID_GRUPO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20003, 'Erro: Campos obrigatórios não preenchidos');
    END IF;
END;
/

CREATE TABLE REACAO_GRUPO (
    ID_MENSAGEM INT,
    ID_USER_REAGE INT,
    REACAO VARCHAR(20)
);

ALTER TABLE REACAO_GRUPO ADD CONSTRAINT FK_REACAO_GRUPO_MENSAGEM FOREIGN KEY (ID_MENSAGEM) REFERENCES MENSAGEM_GRUPO(ID_MENSAGEM);
ALTER TABLE REACAO_GRUPO ADD CONSTRAINT FK_REACAO_GRUPO_USER FOREIGN KEY (ID_USER_REAGE) REFERENCES PARTICIPA_DE(ID_USER);


CREATE TABLE USUARIO (
    ID_USER INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME VARCHAR(25),
    STATUS VARCHAR(100),
    DATA_NASCIMENTO DATE,
    EMAIL VARCHAR(50) UNIQUE,
    SENHA VARCHAR(50)
);

-- Permite criação de usuários sem status, porém os outros campos são obrigatórios
CREATE TRIGGER USUARIO_VAZIO_INSERT
BEFORE INSERT ON USUARIO FOR EACH ROW
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, campos obrigatórios não preenchidos')
    WHERE
        NEW.NOME IS NULL OR
        NEW.DATA_NASCIMENTO IS NULL OR
        NEW.EMAIL IS NULL OR
        NEW.SENHA IS NULL;
END;
CREATE TRIGGER USUARIO_VAZIO_UPDATE
BEFORE UPDATE ON USUARIO FOR EACH ROW
BEGIN
    SELECT 
        RAISE(ABORT, 'Erro, campos obrigatórios não preenchidos')
    WHERE
        NEW.NOME IS NULL OR
        NEW.DATA_NASCIMENTO IS NULL OR
        NEW.EMAIL IS NULL OR
        NEW.SENHA IS NULL;
END;


CREATE TABLE MENSAGEM_PRIVADA (
    ID_MENSAGEM INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_USER_ORIGEM INTEGER,
    ID_USER_DESTINO INTEGER,
    CONTEUDO VARCHAR(250),
    DATA_ENVIO DATETIME,
    STATUS VARCHAR(20),
    REACAO VARCHAR(20),
    CONSTRAINT FK_MENSAGEM_PRIVADA_ORIGEM FOREIGN KEY (ID_USER_ORIGEM) REFERENCES USUARIO(ID_USER),
    CONSTRAINT FK_MENSAGEM_PRIVADA_DESTINO FOREIGN KEY (ID_USER_DESTINO) REFERENCES USUARIO(ID_USER)
);

CREATE TRIGGER MENSAGEM_PRIVADA_VAZIA
BEFORE INSERT ON MENSAGEM_PRIVADA FOR EACH ROW
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, mensagem vazia')
    WHERE
        NEW.CONTEUDO IS NULL;
END;

--CREATE OR REPLACE TRIGGER MENSAGEM_PRIVADA_VAZIA
--BEFORE INSERT ON MENSAGEM_PRIVADA
--BEGIN
--    IF (:NEW.CONTEUDO IS NULL) THEN
--        RAISE_APPLICATION_ERROR(-20001, 'Erro: Mensagem vazia');
--    END IF;
--END;

CREATE TABLE MENSAGEM_GRUPO (
    ID_MENSAGEM INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_USER_ORIGEM INTEGER,
    ID_GRUPO_DESTINO INTEGER,
    CONTEUDO VARCHAR(250),
    DATA_ENVIO DATE,
    CONSTRAINT FK_MENSAGEM_GRUPO_ORIGEM FOREIGN KEY (ID_USER_ORIGEM) REFERENCES USUARIO(ID_USER),
    CONSTRAINT FK_MENSAGEM_GRUPO_DESTINO FOREIGN KEY (ID_GRUPO_DESTINO) REFERENCES GRUPO(ID_GRUPO)
);

--ALTER TABLE MENSAGEM_GRUPO ADD CONSTRAINT FK_MENSAGEM_GRUPO_ORIGEM FOREIGN KEY (ID_USER_ORIGEM) REFERENCES USUARIO(ID_USER);
--ALTER TABLE MENSAGEM_GRUPO ADD CONSTRAINT FK_MENSAGEM_GRUPO_DESTINO FOREIGN KEY (ID_GRUPO_DESTINO) REFERENCES GRUPO(ID_GRUPO);

CREATE TRIGGER MENSAGEM_GRUPO_VAZIA
BEFORE INSERT ON MENSAGEM_GRUPO
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, mensagem vazia')
    WHERE
        NEW.CONTEUDO IS NULL;
END;

/*CREATE OR REPLACE TRIGGER MENSAGEM_GRUPO_VAZIA
BEFORE INSERT ON MENSAGEM_GRUPO
BEGIN
    IF (:NEW.CONTEUDO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20001, 'Erro: Mensagem vazia');
    END IF;
END;
/*/

CREATE TABLE GRUPO (
    ID_GRUPO INTEGER PRIMARY KEY AUTOINCREMENT,
    DESCRICAO VARCHAR(100),
    DATA_CRIACAO DATE,
    NOME_GRUPO VARCHAR(25)
);

CREATE TRIGGER GRUPO_VAZIO_INSERT
BEFORE INSERT ON GRUPO
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, nome do grupo vazio')
    WHERE
        NEW.NOME_GRUPO IS NULL;
END;

/*CREATE OR REPLACE TRIGGER GRUPO_VAZIO
BEFORE INSERT ON GRUPO
BEGIN
    IF (:NEW.NOME_GRUPO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20002, 'Erro: Nome do grupo vazio');
    END IF;
END;
/*/

CREATE TABLE PARTICIPA_DE (
    ID_USER INTEGER,
    ID_GRUPO INTEGER,
    ADMINISTRADOR BOOLEAN,
    CONSTRAINT FK_PARTICIPA_DE_USUARIO FOREIGN KEY (ID_USER) REFERENCES USUARIO(ID_USER),
    CONSTRAINT FK_PARTICIPA_DE_GRUPO FOREIGN KEY (ID_GRUPO) REFERENCES GRUPO(ID_GRUPO)
);

/*ALTER TABLE PARTICIPA_DE ADD CONSTRAINT FK_PARTICIPA_DE_USUARIO FOREIGN KEY (ID_USER) REFERENCES USUARIO(ID_USER);
ALTER TABLE PARTICIPA_DE ADD CONSTRAINT FK_PARTICIPA_DE_GRUPO FOREIGN KEY (ID_GRUPO) REFERENCES GRUPO(ID_GRUPO);*/

CREATE TRIGGER PARTICIPA_DE_VAZIO
BEFORE INSERT ON PARTICIPA_DE
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, campos obrigatórios não preenchidos')
    WHERE
        NEW.ID_USER IS NULL OR
        NEW.ID_GRUPO IS NULL;
END;

/*CREATE OR REPLACE TRIGGER PARTICIPA_DE_VAZIO
BEFORE INSERT ON PARTICIPA_DE
BEGIN
    IF (:NEW.ID_USER IS NULL OR
        :NEW.ID_GRUPO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20003, 'Erro: Campos obrigatórios não preenchidos');
    END IF;
END;
/*/

CREATE TABLE REACAO_GRUPO (
    ID_MENSAGEM INTEGER,
    ID_USER_REAGE INTEGER,
    REACAO VARCHAR(20),
    CONSTRAINT FK_REACAO_GRUPO_MENSAGEM FOREIGN KEY (ID_MENSAGEM) REFERENCES MENSAGEM_GRUPO(ID_MENSAGEM),
    CONSTRAINT FK_REACAO_GRUPO_USER FOREIGN KEY (ID_USER_REAGE) REFERENCES PARTICIPA_DE(ID_USER)
);

--ALTER TABLE REACAO_GRUPO ADD CONSTRAINT FK_REACAO_GRUPO_MENSAGEM FOREIGN KEY (ID_MENSAGEM) REFERENCES MENSAGEM_GRUPO(ID_MENSAGEM);
--ALTER TABLE REACAO_GRUPO ADD CONSTRAINT FK_REACAO_GRUPO_USER FOREIGN KEY (ID_USER_REAGE) REFERENCES PARTICIPA_DE(ID_USER);
CREATE TABLE USUARIO (
    ID_USER INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME VARCHAR(25),
    STATUS VARCHAR(100),
    DATA_NASCIMENTO DATE,
    EMAIL VARCHAR(50) UNIQUE,
    SENHA VARCHAR(50)
);

-- Permite criação de usuários sem status, porém os outros campos são obrigatórios
CREATE TRIGGER USUARIO_VAZIO_INSERT
BEFORE INSERT ON USUARIO FOR EACH ROW
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, campos obrigatórios não preenchidos')
    WHERE
        NEW.NOME IS NULL OR
        NEW.DATA_NASCIMENTO IS NULL OR
        NEW.EMAIL IS NULL OR
        NEW.SENHA IS NULL;
END;
CREATE TRIGGER USUARIO_VAZIO_UPDATE
BEFORE UPDATE ON USUARIO FOR EACH ROW
BEGIN
    SELECT 
        RAISE(ABORT, 'Erro, campos obrigatórios não preenchidos')
    WHERE
        NEW.NOME IS NULL OR
        NEW.DATA_NASCIMENTO IS NULL OR
        NEW.EMAIL IS NULL OR
        NEW.SENHA IS NULL;
END;


CREATE TABLE MENSAGEM_PRIVADA (
    ID_MENSAGEM INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_USER_ORIGEM INTEGER,
    ID_USER_DESTINO INTEGER,
    CONTEUDO VARCHAR(250),
    DATA_ENVIO DATETIME,
    STATUS VARCHAR(20),
    REACAO VARCHAR(20),
    CONSTRAINT FK_MENSAGEM_PRIVADA_ORIGEM FOREIGN KEY (ID_USER_ORIGEM) REFERENCES USUARIO(ID_USER),
    CONSTRAINT FK_MENSAGEM_PRIVADA_DESTINO FOREIGN KEY (ID_USER_DESTINO) REFERENCES USUARIO(ID_USER)
);

CREATE TRIGGER MENSAGEM_PRIVADA_VAZIA
BEFORE INSERT ON MENSAGEM_PRIVADA FOR EACH ROW
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, mensagem vazia')
    WHERE
        NEW.CONTEUDO IS NULL;
END;

--CREATE OR REPLACE TRIGGER MENSAGEM_PRIVADA_VAZIA
--BEFORE INSERT ON MENSAGEM_PRIVADA
--BEGIN
--    IF (:NEW.CONTEUDO IS NULL) THEN
--        RAISE_APPLICATION_ERROR(-20001, 'Erro: Mensagem vazia');
--    END IF;
--END;

CREATE TABLE MENSAGEM_GRUPO (
    ID_MENSAGEM INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_USER_ORIGEM INTEGER,
    ID_GRUPO_DESTINO INTEGER,
    CONTEUDO VARCHAR(250),
    DATA_ENVIO DATE,
    CONSTRAINT FK_MENSAGEM_GRUPO_ORIGEM FOREIGN KEY (ID_USER_ORIGEM) REFERENCES USUARIO(ID_USER),
    CONSTRAINT FK_MENSAGEM_GRUPO_DESTINO FOREIGN KEY (ID_GRUPO_DESTINO) REFERENCES GRUPO(ID_GRUPO)
);

--ALTER TABLE MENSAGEM_GRUPO ADD CONSTRAINT FK_MENSAGEM_GRUPO_ORIGEM FOREIGN KEY (ID_USER_ORIGEM) REFERENCES USUARIO(ID_USER);
--ALTER TABLE MENSAGEM_GRUPO ADD CONSTRAINT FK_MENSAGEM_GRUPO_DESTINO FOREIGN KEY (ID_GRUPO_DESTINO) REFERENCES GRUPO(ID_GRUPO);

CREATE TRIGGER MENSAGEM_GRUPO_VAZIA
BEFORE INSERT ON MENSAGEM_GRUPO
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, mensagem vazia')
    WHERE
        NEW.CONTEUDO IS NULL;
END;

/*CREATE OR REPLACE TRIGGER MENSAGEM_GRUPO_VAZIA
BEFORE INSERT ON MENSAGEM_GRUPO
BEGIN
    IF (:NEW.CONTEUDO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20001, 'Erro: Mensagem vazia');
    END IF;
END;
/*/

CREATE TABLE GRUPO (
    ID_GRUPO INTEGER PRIMARY KEY AUTOINCREMENT,
    DESCRICAO VARCHAR(100),
    DATA_CRIACAO DATE,
    NOME_GRUPO VARCHAR(25)
);

CREATE TRIGGER GRUPO_VAZIO_INSERT
BEFORE INSERT ON GRUPO
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, nome do grupo vazio')
    WHERE
        NEW.NOME_GRUPO IS NULL;
END;

/*CREATE OR REPLACE TRIGGER GRUPO_VAZIO
BEFORE INSERT ON GRUPO
BEGIN
    IF (:NEW.NOME_GRUPO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20002, 'Erro: Nome do grupo vazio');
    END IF;
END;
/*/

CREATE TABLE PARTICIPA_DE (
    ID_USER INTEGER,
    ID_GRUPO INTEGER,
    ADMINISTRADOR BOOLEAN,
    CONSTRAINT FK_PARTICIPA_DE_USUARIO FOREIGN KEY (ID_USER) REFERENCES USUARIO(ID_USER),
    CONSTRAINT FK_PARTICIPA_DE_GRUPO FOREIGN KEY (ID_GRUPO) REFERENCES GRUPO(ID_GRUPO)
);

/*ALTER TABLE PARTICIPA_DE ADD CONSTRAINT FK_PARTICIPA_DE_USUARIO FOREIGN KEY (ID_USER) REFERENCES USUARIO(ID_USER);
ALTER TABLE PARTICIPA_DE ADD CONSTRAINT FK_PARTICIPA_DE_GRUPO FOREIGN KEY (ID_GRUPO) REFERENCES GRUPO(ID_GRUPO);*/

CREATE TRIGGER PARTICIPA_DE_VAZIO
BEFORE INSERT ON PARTICIPA_DE
BEGIN
    SELECT
        RAISE(ABORT, 'Erro, campos obrigatórios não preenchidos')
    WHERE
        NEW.ID_USER IS NULL OR
        NEW.ID_GRUPO IS NULL;
END;

/*CREATE OR REPLACE TRIGGER PARTICIPA_DE_VAZIO
BEFORE INSERT ON PARTICIPA_DE
BEGIN
    IF (:NEW.ID_USER IS NULL OR
        :NEW.ID_GRUPO IS NULL) THEN
        RAISE_APPLICATION_ERROR(-20003, 'Erro: Campos obrigatórios não preenchidos');
    END IF;
END;
/*/

CREATE TABLE REACAO_GRUPO (
    ID_MENSAGEM INTEGER,
    ID_USER_REAGE INTEGER,
    REACAO VARCHAR(20),
    CONSTRAINT FK_REACAO_GRUPO_MENSAGEM FOREIGN KEY (ID_MENSAGEM) REFERENCES MENSAGEM_GRUPO(ID_MENSAGEM),
    CONSTRAINT FK_REACAO_GRUPO_USER FOREIGN KEY (ID_USER_REAGE) REFERENCES PARTICIPA_DE(ID_USER)
);

--ALTER TABLE REACAO_GRUPO ADD CONSTRAINT FK_REACAO_GRUPO_MENSAGEM FOREIGN KEY (ID_MENSAGEM) REFERENCES MENSAGEM_GRUPO(ID_MENSAGEM);
--ALTER TABLE REACAO_GRUPO ADD CONSTRAINT FK_REACAO_GRUPO_USER FOREIGN KEY (ID_USER_REAGE) REFERENCES PARTICIPA_DE(ID_USER);
