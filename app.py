from flask import Flask, jsonify, request
import sqlite3

# Configuração do Flask
app = Flask(__name__)

# Caminho para o banco de dados
DATABASE = "filmes.db"

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Retorna as linhas como dicionários
    return conn

# Rota para listar todos os filmes
@app.route("/api/filmes", methods=["GET"])
def listar_filmes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM filmes")
    filmes = cursor.fetchall()
    conn.close()
    return jsonify([dict(filme) for filme in filmes])

# Rota para buscar um filme por ID
@app.route("/api/filmes/<int:id>", methods=["GET"])
def buscar_filme(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM filmes WHERE id = ?", (id,))
    filme = cursor.fetchone()
    conn.close()
    if filme:
        return jsonify(dict(filme))
    else:
        return jsonify({"error": "Filme não encontrado"}), 404

# Rota para adicionar um novo filme
@app.route("/api/filmes", methods=["POST"])
def adicionar_filme():
    novo_filme = request.get_json()
    if not novo_filme:
        return jsonify({"error": "Dados inválidos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO filmes (titulo, ano, duracao, classificacao, imdb, sinopse, generos, qualidade, player)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        novo_filme.get("titulo"),
        novo_filme.get("ano"),
        novo_filme.get("duracao"),
        novo_filme.get("classificacao"),
        novo_filme.get("imdb"),
        novo_filme.get("sinopse"),
        novo_filme.get("generos"),
        novo_filme.get("qualidade"),
        novo_filme.get("player")
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Filme adicionado com sucesso!"}), 201

# Rota para atualizar um filme existente
@app.route("/api/filmes/<int:id>", methods=["PUT"])
def atualizar_filme(id):
    dados_atualizados = request.get_json()
    if not dados_atualizados:
        return jsonify({"error": "Dados inválidos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE filmes
        SET titulo = ?, ano = ?, duracao = ?, classificacao = ?, imdb = ?, sinopse = ?, generos = ?, qualidade = ?, player = ?
        WHERE id = ?
    ''', (
        dados_atualizados.get("titulo"),
        dados_atualizados.get("ano"),
        dados_atualizados.get("duracao"),
        dados_atualizados.get("classificacao"),
        dados_atualizados.get("imdb"),
        dados_atualizados.get("sinopse"),
        dados_atualizados.get("generos"),
        dados_atualizados.get("qualidade"),
        dados_atualizados.get("player"),
        id
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Filme atualizado com sucesso!"})

# Rota para deletar um filme
@app.route("/api/filmes/<int:id>", methods=["DELETE"])
def deletar_filme(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM filmes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Filme deletado com sucesso!"})

# Iniciar o servidor Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)