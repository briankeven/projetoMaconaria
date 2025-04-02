from flask import Flask, render_template, request,redirect, session, flash, jsonify
import os
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.secret_key = '12345'
CORS(app)

def conectar_db():
    conectar = sqlite3.connect('MeuBanco.db')
    return conectar

def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS eventos (id INTEGER PRIMARY KEY AUTOINCREMENT, mes INT, dia INT, desc TEXT)')
    conectar.commit()
    conectar.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/administracao')
def administracao():
    return render_template('adm.html')

@app.route('/calendario')
def calendario():
    return render_template('calendario.html')

@app.route('/editCalendario')
def editCalendario():
    return render_template('editCalendario.html')


    

@app.route("/adicionar", methods=["POST"])

def adicionar_usuario():

    try:    
        criar_tabela()
        dados = request.get_json()
        if not dados or "mes" not in dados or "dia" not in dados or "desc" not in dados:
            return jsonify({"Erro": "formato inválido"}), 400
        
        mes = dados["mes"]
        dia = dados["dia"]
        desc = dados["desc"]

        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute('INSERT INTO eventos (mes, dia, desc) VALUES (?, ?, ?)', (mes, dia, desc))
        conectar.commit()
        conectar.close()
        return jsonify ({"mensagem": "Usuário adicionado com sucesso"}), 200
    except Exception as e:
        print('Erro no servidor:', str(e))
        return jsonify({"Erro": "Erro interno do servidor"}), 500

@app.route("/eventos", methods=["GET"])
def listar_eventos():
    try: 
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute('SELECT * FROM eventos')
        eventos = cursor.fetchall()
        conectar.close()
        
        return jsonify(eventos)
    except Exception as e:
        print('Erro no servidor:', str(e))
        return jsonify({"Erro": "Erro interno do servidor"}), 500

@app.route("/deletar", methods=["GET"])
def deletar_tabela():
    try:
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute('DROP TABLE IF EXISTS eventos')
        conectar.commit()
        return jsonify({"mensagem": "Tabela deletada com sucesso!"}), 200
    except Exception as e:
        print("Erro no servidor:", str(e))
        return jsonify({"Erro": "Erro interno do servidor"}), 500
    finally:
        conectar.close()
@app.route("/delLinha", methods=["POST"] )
def deletar_linha():
    try:
        dados = request.get_json()
        evento_id = dados.get("id")
        if evento_id is None:
            return jsonify({"erro": "Id não informado"}), 400
        conectar = conectar_db()
        cursor = conectar.cursor()
        cursor.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
        conectar.commit()

        if cursor.rowcount == 0:
            return jsonify({"erro": "Nenhum evento encontrado com esse ID"}), 404
        
        return jsonify({"Mensagem": "Evento removido com sucesso!"}), 200
    except Exception as e:
        print("Erro no servidor", str(e))
        return jsonify({"erro": "Erro interno do servidor"}), 500
    finally:
        conectar.close()

if __name__ == '__main__':
      app.run(port=5000, host='0.0.0.0', debug=True, threaded=True)