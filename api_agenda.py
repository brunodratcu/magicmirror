from flask import Flask, request, render_template_string
import json
import datetime
import os

import pygame
import time
import json
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = 'agenda.db' #
EVENTS_FILE = "events.json"

@app.route('/')
def form():
    return render_template_string(open("formulario.html").read())

@app.route('/adicionar', methods=['POST'])
def adicionar_evento():
    data = request.form['data']
    titulo = request.form['titulo']

    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'r') as f:
            eventos = json.load(f)
    else:
        eventos = []

    eventos.append({
        'data': data,
        'titulo': titulo
    })

    with open(EVENTS_FILE, 'w') as f:
        json.dump(eventos, f)

    return 'Evento adicionado com sucesso! <a href="/">Voltar</a>'

@app.route('/resetar', methods=['POST'])
def resetar():
    with open(EVENTS_FILE, 'w') as f:
        json.dump([], f)
    return 'Eventos resetados! <a href="/">Voltar</a>'

@app.route('/eventos_hoje')
def eventos_hoje():
    if not os.path.exists(EVENTS_FILE):
        return json.dumps([])

    with open(EVENTS_FILE, 'r') as f:
        eventos = json.load(f)

    hoje = datetime.datetime.now().strftime('%Y-%m-%d')
    eventos_hoje = [e for e in eventos if e['data'] == hoje]
    return json.dumps(eventos_hoje)








# Criação da tabela
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evento TEXT NOT NULL,
                datahora TEXT NOT NULL
            )
        ''')
init_db()

# Rota para adicionar evento
@app.route('/adicionar', methods=['POST'])
def adicionar_evento():
    evento = request.form['evento']
    data = request.form['data']
    hora = request.form['hora']
    datahora_str = f"{data} {hora}"

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('INSERT INTO eventos (evento, datahora) VALUES (?, ?)', (evento, datahora_str))
        return f"Evento '{evento}' adicionado com sucesso para {datahora_str}!"
    except Exception as e:
        return f"Erro ao adicionar: {e}", 500

# Rota para obter eventos de hoje
@app.route('/eventos', methods=['GET'])
def obter_eventos():
    hoje = datetime.now().date().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT evento, datahora FROM eventos WHERE date(datahora) = ?", (hoje,))
        eventos = cursor.fetchall()
    return jsonify(eventos)

# Resetar banco
@app.route('/resetar', methods=['POST'])
def resetar():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
    return "Banco resetado com sucesso."




pygame.init()
screen = pygame.display.set_mode((480, 320))  # ajuste conforme sua tela
pygame.display.set_caption("Magic Mirror")
font_big = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 40)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

EVENTS_FILE = "events.json"
last_mod = 0

def draw_screen():
    screen.fill(BLACK)
    
    now = datetime.now()
    hora = now.strftime("%H:%M")
    data = now.strftime("%d/%m/%Y")

    hora_txt = font_big.render(hora, True, WHITE)
    data_txt = font_small.render(data, True, WHITE)
    screen.blit(hora_txt, (10, 10))
    screen.blit(data_txt, (10, 70))

    eventos = []
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'r') as f:
            eventos = json.load(f)

    y = 120
    hoje = now.strftime('%Y-%m-%d')
    for e in eventos:
        if e['data'] == hoje:
            evento_txt = font_small.render(e['titulo'], True, WHITE)
            screen.blit(evento_txt, (10, y))
            y += 40

    pygame.display.flip()

while True:
    if os.path.exists(EVENTS_FILE):
        mod = os.path.getmtime(EVENTS_FILE)
        if mod != last_mod:
            last_mod = mod
            draw_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    time.sleep(1)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
