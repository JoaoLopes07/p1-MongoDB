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

@app.route('/novo_setor', methods=['POST'])
def novo_setor():
    if request.method == 'POST':
        setor_nome = request.form['nome']
        query = 'INSERT INTO setor (nome) VALUES (%s)'
        db_cursor.execute(query, (setor_nome,))
        connection.commit()
    return redirect(url_for('home'))

@app.route('/novo_cargo', methods=['POST'])
def novo_cargo():
    if request.method == 'POST':
        nome_cargo = request.form['nome_cargo']
        query = 'INSERT INTO cargos (nome) VALUES (%s)'
        db_cursor.execute(query, (nome_cargo,))
        connection.commit()
    return redirect(url_for('home'))

@app.route('/novo_funcionario', methods=['POST'])
def processar_novo_funcionario():
    primeiro_nome = request.form['primeiro_nome']
    sobrenome = request.form['sobrenome']
    data_admissao = request.form['data_admissao']
    status_funcionario = request.form['status_funcionario']
    id_setor = request.form['id_setor']
    id_cargo = request.form['id_cargo']

    # Inserir dados no banco de dados
    db_cursor.execute(
        'INSERT INTO funcionarios (primeiro_nome, sobrenome, data_admissao, status_funcionario, id_setor, id_cargo) VALUES (%s, %s, %s, %s, %s, %s)',
        (primeiro_nome, sobrenome, data_admissao, status_funcionario, id_setor, id_cargo)
    )
    connection.commit()

    return redirect(url_for('home'))

@app.route('/listar_funcionarios')
def listar_funcionarios():
    db_cursor.execute('SELECT * FROM funcionarios')
    funcionarios = db_cursor.fetchall()
    return render_template('listar_funcionarios.html', funcionarios=funcionarios)

@app.route('/editar_funcionario/<int:id>', methods=['GET', 'POST'])
def editar_funcionario(id):
    if request.method == 'POST':
        primeiro_nome = request.form['primeiro_nome']
        sobrenome = request.form['sobrenome']
        data_admissao = request.form['data_admissao']
        status_funcionario = request.form['status_funcionario']
        id_setor = request.form['id_setor']
        id_cargo = request.form['id_cargo']

        # Atualizar dados no banco de dados
        db_cursor.execute(
            'UPDATE funcionarios SET primeiro_nome=%s, sobrenome=%s, data_admissao=%s, status_funcionario=%s, id_setor=%s, id_cargo=%s WHERE id=%s',
            (primeiro_nome, sobrenome, data_admissao, status_funcionario, id_setor, id_cargo, id)
        )
        connection.commit()

        return redirect(url_for('listar_funcionarios'))
    else:
        db_cursor.execute('SELECT * FROM funcionarios WHERE id=%s', (id,))
        funcionario = db_cursor.fetchone()
        return render_template('editar_funcionario.html', funcionario=funcionario)

@app.route('/deletar_funcionario/<int:id>', methods=['POST'])
def deletar_funcionario(id):
    db_cursor.execute('DELETE FROM funcionarios WHERE id=%s', (id,))
    connection.commit()
    return redirect(url_for('listar_funcionarios'))

if __name__ == '__main__':
    app.run(debug=True)