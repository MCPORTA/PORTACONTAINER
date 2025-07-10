from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)

# Configuración de la base de datos
def init_db():
    conn = sqlite3.connect('mecanografia.db')
    cursor = conn.cursor()
    
    # Tabla para resultados de tests
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wpm REAL,
            precision REAL,
            tiempo_total REAL,
            fecha_hora TEXT,
            texto_usado TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Textos para practicar
TEXTOS = [
    "La tecnología avanza a pasos agigantados en el mundo moderno. Cada día surgen nuevas innovaciones que transforman la forma en que vivimos y trabajamos.",
    "El aprendizaje es un proceso continuo que nunca termina. Siempre hay algo nuevo que descubrir y mejorar en nuestras habilidades.",
    "La programación es el arte de crear soluciones digitales. Los desarrolladores utilizan diferentes lenguajes para construir aplicaciones útiles.",
    "La naturaleza nos ofrece belleza y recursos valiosos. Es importante cuidar el medio ambiente para las futuras generaciones.",
    "La música tiene el poder de conectar personas de diferentes culturas. Cada género musical tiene su propia historia y significado.",
    "El deporte promueve la salud física y mental. La actividad regular ayuda a mantener un estilo de vida equilibrado.",
    "La educación es fundamental para el desarrollo personal y profesional. El conocimiento abre puertas a nuevas oportunidades.",
    "La creatividad es una habilidad que se puede desarrollar con práctica. Las ideas innovadoras surgen de la experimentación.",
    "La comunicación efectiva es clave en las relaciones humanas. Escuchar activamente mejora la comprensión mutua.",
    "La perseverancia es esencial para alcanzar metas importantes. Los obstáculos son oportunidades para crecer y aprender."
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/texto-aleatorio', methods=['GET', 'POST'])
def obtener_texto():
    texto = random.choice(TEXTOS)
    return jsonify({'texto': texto})

@app.route('/api/guardar-resultado', methods=['POST'])
def guardar_resultado():
    data = request.json
    wpm = data.get('wpm', 0)
    precision = data.get('precision', 0)
    tiempo_total = data.get('tiempo_total', 0)
    texto_usado = data.get('texto_usado', '')
    
    conn = sqlite3.connect('mecanografia.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO resultados (wpm, precision, tiempo_total, fecha_hora, texto_usado)
        VALUES (?, ?, ?, ?, ?)
    ''', (wpm, precision, tiempo_total, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), texto_usado))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/api/estadisticas')
def obtener_estadisticas():
    conn = sqlite3.connect('mecanografia.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT wpm, precision, fecha_hora FROM resultados ORDER BY fecha_hora DESC LIMIT 10')
    resultados = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'resultados': [
            {
                'wpm': r[0],
                'precision': r[1],
                'fecha': r[2]
            } for r in resultados
        ]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 