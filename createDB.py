import sqlite3
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

conn = sqlite3.connect('magazin.db')

# создаем курсор для работы с базой данных
cur = conn.cursor()



# создаем таблицу users
cur.execute('''CREATE TABLE users
               (id INTEGER PRIMARY KEY,
               name TEXT NOT NULL,
               email TEXT NOT NULL,
               password TEXT NOT NULL)''')
# добавляем одного пользователя
cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", ('John Doe', 'john@example.com', 'password'))

# создаем таблицу catalog
cur.execute('''CREATE TABLE catalog
               (id INTEGER PRIMARY KEY,
               img TEXT NOT NULL,
               title TEXT NOT NULL,
               price REAL NOT NULL)''')

# добавляем пару начальных значений в таблицу catalog
cur.execute("INSERT INTO catalog (img, title, price) VALUES (?, ?, ?)", ('mon.webp', 'Монитор', 10.99))
cur.execute("INSERT INTO catalog (img, title, price) VALUES (?, ?, ?)", ('not.jpg', 'Ноутбук', 99.99))
cur.execute("INSERT INTO catalog (img, title, price) VALUES (?, ?, ?)", ('pk.webp', 'Компьютер', 49.99))
cur.execute("INSERT INTO catalog (img, title, price) VALUES (?, ?, ?)", ('tel.webp', 'Телефон', 49.99))
cur.execute("INSERT INTO catalog (img, title, price) VALUES (?, ?, ?)", ('prin.webp', 'Принтер', 19.99))
cur.execute("INSERT INTO catalog (img, title, price) VALUES (?, ?, ?)", ('plan.webp', 'Планшет', 129.99))
cur.execute("INSERT INTO catalog (img, title, price) VALUES (?, ?, ?)", ('fot.webp', 'Фотоаппарат', 129.99))
cur.execute("INSERT INTO catalog (img, title, price) VALUES (?, ?, ?)", ('teli.webp', 'Телевизор', 129.99))

# сохраняем изменения в базе данных
conn.commit()

# закрываем соединение с базой данных
conn.close()
