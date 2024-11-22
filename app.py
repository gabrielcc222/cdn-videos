from flask import Flask, request, jsonify, send_from_directory, render_template
import os
import uuid

app = Flask(__name__)

# Configurações
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Cria a pasta de uploads caso não exista
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 1024  # Limite de 1GB por arquivo

# Rota principal
@app.route('/')
def home():
    return render_template('index.html')  # Frontend já criado

# Rota para upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Arquivo inválido'}), 400

    # Salva o arquivo com um nome único
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)

    # Gera um link para download
    file_url = f"{request.host_url}download/{unique_filename}"
    return jsonify({'message': 'Upload concluído!', 'file_url': file_url}), 200

# Rota para download
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Rota para listar todos os arquivos (opcional)
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    file_urls = [f"{request.host_url}download/{file}" for file in files]
    return jsonify({'files': file_urls}), 200

if __name__ == '__main__':
    app.run(debug=True)
