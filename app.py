from flask import Flask, request, send_from_directory
import subprocess, os

app = Flask(__name__)
PASTA = "/sdcard/Download"

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
    tipo = dados.get('tipo','musica')
    # Sem ffmpeg, direto
    if tipo == 'musica':
        cmd = ['yt-dlp','--no-warnings','-f','140/bestaudio','-o',f'{PASTA}/%(title)s.%(ext)s',link]
    else:
        cmd = ['yt-dlp','--no-warnings','-f','best[ext=mp4]/best','-o',f'{PASTA}/%(title)s.%(ext)s',link]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout)
    print(r.stderr)
    if r.returncode==0:
        return {"ok":True,"msg":"Baixado! Olha seu Download!"}
    return {"erro":r.stderr[-400:]},500

app.run(host='0.0.0.0', port=8000)
