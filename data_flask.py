from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/recent_cities', methods=['GET'])
def get_recent_cities():
    # Połączenie z bazą danych
    conn = sqlite3.connect('recent_data.db')
    cursor = conn.cursor()

    # Pobranie danych z bazy
    cursor.execute('SELECT * FROM recent_cities')
    data = cursor.fetchall()

    # Zamknięcie połączenia
    conn.close()

    # Konwersja danych do formatu JSON i zwrócenie jako odpowiedź
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='192.168.5.199', port=5000, debug=True)


