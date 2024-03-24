from flask import Flask, request, redirect, render_template, jsonify
import sqlite3
import string
import random

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_url TEXT NOT NULL,
        visits INTEGER DEFAULT 0
    );
    ''')
    conn.commit()
    conn.close()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for i in range(6))
    return short_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    short_url = generate_short_url()

    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO links (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
    conn.commit()
    conn.close()

    return jsonify({'short_url': short_url})

@app.route('/<short_url>')
def redirect_url(short_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT original_url FROM links WHERE short_url = ?', (short_url,))
    result = cursor.fetchone()

    if result:
        original_url = result[0]
        cursor.execute('UPDATE links SET visits = visits + 1 WHERE short_url = ?', (short_url,))
        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        conn.close()
        return 'URL not found', 404

@app.route('/stats/<short_url>')
def get_stats(short_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT visits FROM links WHERE short_url = ?', (short_url,))
    result = cursor.fetchone()
    conn.close()

    if result:
        visits = result[0]
        return jsonify({'visits': visits})
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
