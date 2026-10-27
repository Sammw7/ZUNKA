from flask import Flask, request, send_from_directory, send_file, jsonify
import subprocess, os, glob, uuid
app = Flask(__name__)
TMP = "/tmp/zunka_dl"
os.makedirs(TMP, exist_ok=True)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
@app.route('/<path:path>')
def arquivos(path):
    return send_from_directory('.', path)
@app.route('/baixar', methods=['POST'])
def baixar():
    dados = request.json
    link = dados.get('url')
    tipo = dados.get('tipo', 'musica')
    if not link:
        return jsonify({"erro": "sem link"}), 400
    uid = str(uuid.uuid4())[:8]
    pasta = os.path.join(TMP, uid)
    os.makedirs(pasta, exist_ok=True)
    base = ['yt-dlp','--no-warnings','--extractor-args','youtube:player_client=ios','--extractor-args','youtube:player_skip=webpage']
    if tipo == 'musica':
        cmd = base + ['-f','140/bestaudio','-o',f'{pasta}/%(title)s.%(ext)s',link]
    else:
        cmd = base + ['-f','best[ext=mp4]/best','-o',f'{pasta}/%(title)s.%(ext)s',link]
    r = subprocess.run(cmd, capture_output=True, text=True)
    arquivos = glob.glob(pasta + "/*")
    if not arquivos or r.returncode != 0:
        return jsonify({"erro": r.stderr[-500:]}), 500
    arquivo = arquivos[0]
    nome = os.path.basename(arquivo)
    resp = send_file(arquivo, as_attachment=True, download_name=nome)
    resp.headers['X-Filename'] = nome
    return resp
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
