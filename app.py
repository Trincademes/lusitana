from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///modelo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Diretório para armazenar uploads

# Criação do diretório de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)

# Modelo
class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False)
    hora = db.Column(db.Integer, nullable=False)  # Nova coluna para a hora
    minuto = db.Column(db.Integer, nullable=False)  # Nova coluna para o minuto
    apresentacao = db.Column(db.String(100), nullable=False)
    agendamento = db.Column(db.String(100), nullable=False)
    tipo_operacao = db.Column(db.String(100), nullable=False)
    numero_bs = db.Column(db.String(100), nullable=False)
    numero_nf = db.Column(db.String(100), nullable=False)
    transportadora = db.Column(db.String(100), nullable=False)
    tipo_veiculo = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(100), nullable=False)
    placa_cavalo = db.Column(db.String(100), nullable=False)
    placa_carreta = db.Column(db.String(100), nullable=False)
    numero_container = db.Column(db.String(100), nullable=False)
    documentos = db.Column(db.String(500), nullable=True)  # Armazena os nomes dos arquivos como uma string


# Criação das tabelas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    modelos = Modelo.query.all()
    return render_template('index.html', modelos=modelos)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        documentos = request.files.getlist('documentos')
        document_names = []

        for doc in documentos:
            if doc:
                # Salva o arquivo no diretório especificado
                doc.save(os.path.join(app.config['UPLOAD_FOLDER'], doc.filename))
                document_names.append(doc.filename)  # Armazena o nome do arquivo

        novo_modelo = Modelo(
            data=datetime.strptime(request.form['data'], '%Y-%m-%d'),
            hora=request.form['hora'],
            minuto=request.form['minuto'],
            apresentacao=request.form['apresentacao'],
            agendamento=request.form['agendamento'],
            tipo_operacao=request.form['tipo_operacao'],
            numero_bs=request.form['numero_bs'],
            numero_nf=request.form['numero_nf'],
            transportadora=request.form['transportadora'],
            tipo_veiculo=request.form['tipo_veiculo'],
            cpf=request.form['cpf'],
            placa_cavalo=request.form['placa_cavalo'],
            placa_carreta=request.form['placa_carreta'],
            numero_container=request.form['numero_container'],
            documentos=','.join(document_names)  # Armazena os nomes dos arquivos como uma string
        )
        db.session.add(novo_modelo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('adicionar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    modelo = Modelo.query.get_or_404(id)
    
    if request.method == 'POST':
        documentos = request.files.getlist('documentos')
        # Preservar documentos antigos ao editar
        document_names = modelo.documentos.split(',') if modelo.documentos else []

        for doc in documentos:
            if doc:
                # Salva o arquivo no diretório especificado
                doc.save(os.path.join(app.config['UPLOAD_FOLDER'], doc.filename))
                document_names.append(doc.filename)  # Armazena o nome do arquivo

        modelo.data = datetime.strptime(request.form['data'], '%Y-%m-%d')
        modelo.hora = request.form['hora']
        modelo.minuto = request.form['minuto']
        modelo.apresentacao = request.form['apresentacao']
        modelo.agendamento = request.form['agendamento']
        modelo.tipo_operacao = request.form['tipo_operacao']
        modelo.numero_bs = request.form['numero_bs']
        modelo.numero_nf = request.form['numero_nf']
        modelo.transportadora = request.form['transportadora']
        modelo.tipo_veiculo = request.form['tipo_veiculo']
        modelo.cpf = request.form['cpf']
        modelo.placa_cavalo = request.form['placa_cavalo']
        modelo.placa_carreta = request.form['placa_carreta']
        modelo.numero_container = request.form['numero_container']
        modelo.documentos = ','.join(document_names)  # Atualiza os nomes dos arquivos

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', modelo=modelo)

if __name__ == '__main__':
    app.run(debug=True)
