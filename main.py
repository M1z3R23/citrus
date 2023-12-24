import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS  # Import the CORS module
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for all route
conn = sqlite3.connect('magazin.db')

# создание пользователя
@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
    conn.commit()

    return f"User {name} with email {email} has been created."

# удаление пользователя
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

    return f"User with ID {user_id} has been deleted."

# получение всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    return {'users': users}

# обновление пользователя
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()

    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    cur.execute("UPDATE users SET name = ?, email = ?, password = ? WHERE id = ?", (name, email, password, user_id))
    conn.commit()

    return f"User with ID {user_id} has been updated."
# получение конкретного пользователя
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cur.fetchone()

    if not user:
        return f"User with ID {user_id} not found."

    return {'user': user}

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password))
    user = cur.fetchone()

    if not user:
        return "Invalid credentials", 401

    return {'user_id': user[0]}

@app.route('/katalog', methods=['GET'])
def get_katalog():
    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()

    # Выполняем запрос для получения всего каталога
    cur.execute("SELECT * FROM catalog")
    
    # Извлекаем все строки из результата запроса
    rows = cur.fetchall()

    # Создаем пустой список для хранения элементов каталога
    catalog = []

    # Итерируемся по строкам результата запроса и формируем словари для каждого элемента каталога
    for row in rows:
        catalog_item = {
            'img': row[1],
            'title': row[2],
            'price': row[3]
        }
        catalog.append(catalog_item)

    # Закрываем соединение с базой данных
    conn.close()

    # Превращаем список элементов каталога в JSON и отправляем обратно в ответе
    return jsonify(catalog)

@app.route('/katalog', methods=['POST'])
def add_katalog():
    conn = sqlite3.connect('magazin.db')
    cur = conn.cursor()

    # Проверяем, что метод запроса - POST
    if request.method == 'POST':
        # Получаем данные из запроса
        img = request.form['img']
        title = request.form['title']
        price = request.form['price']

        # Выполняем запрос для добавления элемента в каталог
        cur.execute("INSERT INTO catalog (img, title, price) VALUES (?, ?, ?)", (img, title, price))
        conn.commit()

    # Выполняем запрос для получения всего каталога
    cur.execute("SELECT * FROM catalog")
    
    # Извлекаем все строки из результата запроса
    rows = cur.fetchall()

    # Создаем пустой список для хранения элементов каталога
    catalog = []

    # Итерируемся по строкам результата запроса и формируем словари для каждого элемента каталога
    for row in rows:
        catalog_item = {
            'img': row[1],
            'title': row[2],
            'price': row[3]
        }
        catalog.append(catalog_item)

    # Закрываем соединение с базой данных
    conn.close()

    # Превращаем список элементов каталога в JSON и отправляем обратно в ответе
    return jsonify(catalog)


if __name__ == '__main__':
    app.run(debug=True)