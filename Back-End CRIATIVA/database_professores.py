# Importa a biblioteca sqlite3 para trabalhar com o banco de dados
import sqlite3

# Importa funções para gerar e verificar hashes de senhas
from werkzeug.security import generate_password_hash, check_password_hash


# Cria e configura uma conexão com o banco de dados
def criar_conexao():
    # Conecta ao banco de dados banco.db
    conexao = sqlite3.connect("banco.db")

    # Permite acessar os dados das consultas pelo nome das colunas
    conexao.row_factory = sqlite3.Row

    # Ativa a verificação das chaves estrangeiras no SQLite
    conexao.execute("PRAGMA foreign_keys = ON")

    # Retorna a conexão criada
    return conexao
    


# Cria a tabela professores caso ela ainda não exista
def criar_banco_professores():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Cria a tabela professores com suas colunas e chave estrangeira
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            id_escola_fk INTEGER NOT NULL,
            
            
            FOREIGN KEY(id_escola_fk)
            REFERENCES escolas(id_escola)
        )
    """)

    # Salva as alterações no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()


# Adiciona um novo professor ao banco de dados
def adicionar_professor(nome, email, senha,id_escola_fk):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Gera um hash da senha para não armazená-la em texto puro
    senha_hash = generate_password_hash(senha)

    # Insere o nome, o email, a senha criptografada em hash
    # e o ID da escola do professor na tabela
    cursor.execute("""
        INSERT INTO professores (nome, email, senha, id_escola_fk)
        VALUES (?, ?, ?, ?)
    """, (nome, email, senha_hash,id_escola_fk))

    # Salva o cadastro no banco de dados
    conexao.commit()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna o nome do professor cadastrado
    return nome


# Lista todos os professores cadastrados
def listar_professores():
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona o ID, o nome e o email dos professores
    # A senha não é incluída nessa consulta
    cursor.execute("""
        SELECT id_professor, nome, email
        FROM professores
    """)

    # Recupera todos os professores encontrados
    professores = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Converte os registros em dicionários e retorna a lista
    return [dict(professor) for professor in professores]


# Edita os dados de um professor pelo seu ID
def editar_professor(id_professor, nome, email, senha):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Gera um hash para a nova senha informada
    senha_hash = generate_password_hash(senha)

    # Atualiza o nome, o email e a senha do professor
    # correspondente ao ID informado
    cursor.execute("""
        UPDATE professores
        SET nome = ?, email = ?, senha = ?, id_escola_fk = ?
        WHERE id_professor = ?
    """, (nome, email, senha_hash, id_professor))

    # Salva as alterações no banco de dados
    conexao.commit()

    # Recupera a quantidade de registros afetados pela atualização
    linhas_afetadas = cursor.rowcount

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a quantidade de registros atualizados
    return linhas_afetadas


# Exclui um professor pelo seu ID
def excluir_professor(id_professor):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Exclui o professor que possui o ID informado
    cursor.execute("""
        DELETE FROM professores
        WHERE id_professor = ?
    """, (id_professor,))

    # Salva a exclusão no banco de dados
    conexao.commit()

    # Recupera a quantidade de registros afetados pela exclusão
    linhas_afetadas = cursor.rowcount

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna a quantidade de registros excluídos
    return linhas_afetadas


# Verifica se o email e a senha informados são válidos
def verificar_login_professores(email, senha):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Busca o professor que possui o email informado
    cursor.execute("""
        SELECT id_professor, nome, email, senha
        FROM professores
        WHERE email = ?
    """, (email,))

    # Recupera o primeiro professor encontrado
    professor = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Se o professor não existir, retorna None
    if professor is None:
        return None

    # Compara a senha informada com o hash armazenado
    # Se a senha estiver incorreta, retorna None
    if not check_password_hash(professor["senha"], senha):
        return None

    # Se o login for válido, retorna os dados do professor
    # A senha não é incluída no retorno
    return {
        "id_professor": professor["id_professor"],
        "nome": professor["nome"],
        "email": professor["email"]
    }


# Busca um professor pelo seu ID
def buscar_professor_por_id(id_professor):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona todos os dados do professor correspondente ao ID
    cursor.execute("""
        SELECT id_professor, nome, email
        FROM professores
        WHERE id_professor = ?
    """, (id_professor,))

    # Recupera o professor encontrado
    professor = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Retorna os dados como dicionário se o professor existir
    # Caso contrário, retorna None
    return dict(professor) if professor else None


# Lista os professores que pertencem a uma determinada escola
def listar_professores_por_escola(id_escola):
    # Cria uma conexão com o banco de dados
    conexao = criar_conexao()

    # Cria um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Seleciona o ID e o nome dos professores
    # vinculados à escola informada
    cursor.execute("""
        SELECT id_professor,nome 
        FROM professores
        WHERE id_escola_fk = ?
    """, (id_escola,))

    # Recupera todos os professores encontrados
    professores = cursor.fetchall()

    # Fecha a conexão com o banco de dados
    conexao.close()

    # Converte os registros em dicionários e retorna a lista
    return [dict(professor) for professor in professores]
