import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('users.db')
cursor = connection.cursor()

# Выполнение запроса
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

# Вывод результатов
for row in rows:
    print(row)

# Закрытие соединения
cursor.close()
connection.close()