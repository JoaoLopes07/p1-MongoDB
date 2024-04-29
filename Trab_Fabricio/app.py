from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

connection = mysql.connector.connect(
    host='localhost',
    user='lopesserver',
    password='jv070404',
    database='aula_13_10'
)

db_cursor = connection.cursor()

@app.route('/')
def home():
    return render_template('trab.html')

@app.route('/novo_funcionario', methods=['POST'])
def processar_novo_funcionario():
    primeiro_nome = request.form['primeiro_nome']
    sobrenome = request.form['sobrenome']
    data_admissao = request.form['data_admissao']
    status_funcionario = request.form['status_funcionario']
    
    # Inserir dados no banco de dados
    db_cursor.execute(
        'INSERT INTO funcionarios (primeiro_nome, sobrenome, data_admissao, status_funcionario) VALUES (%s, %s, %s, %s)',
        (primeiro_nome, sobrenome, data_admissao, status_funcionario)
    )
    connection.commit()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
