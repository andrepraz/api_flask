import sqlite3

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# ==========================
# Conexão com SQLite
# ==========================

def conectar():

    return sqlite3.connect(
        "clientes.sqlite"
    )


# ==========================
# Criação da Tabela
# ==========================

def criar_tabela():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS cliente(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT NOT NULL

        )

    """)

    conn.commit()
    conn.close()


criar_tabela()

# ==========================
# Página Principal
# ==========================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ==========================
# LISTAR
# ==========================

@app.route("/clientes",
           methods=["GET"])
def listar_clientes():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM cliente"
    )

    registros = cursor.fetchall()

    conn.close()

    lista = []

    for item in registros:

        lista.append({
            "id": item[0],
            "nome": item[1],
            "telefone": item[2],
            "cpf": item[3]
        })

    return jsonify(lista)


# ==========================
# INSERIR
# ==========================

@app.route("/clientes",
           methods=["POST"])
def inserir_cliente():

    dados = request.json

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO cliente(
            nome,
            telefone,
            cpf
        )

        VALUES(
            ?,
            ?,
            ?
        )

    """, (

        dados["nome"],
        dados["telefone"],
        dados["cpf"]

    ))

    conn.commit()
    conn.close()

    return jsonify({
        "mensagem":
        "Cliente inserido"
    })


# ==========================
# ALTERAR
# ==========================

@app.route("/clientes/<int:id>",
           methods=["PUT"])
def alterar_cliente(id):

    dados = request.json

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE cliente

        SET

            nome=?,
            telefone=?,
            cpf=?

        WHERE id=?

    """, (

        dados["nome"],
        dados["telefone"],
        dados["cpf"],
        id

    ))

    conn.commit()
    conn.close()

    return jsonify({
        "mensagem":
        "Cliente atualizado"
    })


# ==========================
# EXCLUIR
# ==========================

@app.route("/clientes/<int:id>",
           methods=["DELETE"])
def excluir_cliente(id):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM cliente WHERE id=?",

        (id,)

    )

    conn.commit()
    conn.close()

    return jsonify({
        "mensagem":
        "Cliente removido"
    })


if __name__ == "__main__":

    app.run(
        debug=True
    )