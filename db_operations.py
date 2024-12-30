from logging_config import setup_logger
import sqlite3

connection = sqlite3.connect('users.db')
logger = setup_logger()

cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (telegram_id BIGING)')
connection.commit()
cursor.close()

def add_user(telegram_id):
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        data = cursor.fetchall()
        
        if len(data) != 0:
            logger.info(f'Данный пользователь с id - {telegram_id} уже существует')
            cursor.close()
            return False

        cursor.execute('INSERT INTO users (telegram_id) VALUES (?) ', (telegram_id,))
        logger.info(f'В базу данных добавлен пользователь: {telegram_id}')
        connection.commit()
        return True
    except Exception as e:
        logger.info(f'Ошибка при добавлении нового пользователя: {e}')
        return False
    finally:
        cursor.close()

def delete_user(telegram_id):
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        data = cursor.fetchall()
        
        if len(data) == 0:
            logger.info(f'Пользователь с id - {telegram_id} не найден в базе данных')
            return False  # Пользователь не найден

        # Удаляем пользователя
        cursor.execute('DELETE FROM users WHERE telegram_id = ?', (telegram_id,))
        connection.commit()
        logger.info(f'Пользователь с id - {telegram_id} удалён из базы данных')
        return True  # Пользователь успешно удалён
    except Exception as e:
        logger.error(f'Ошибка при удалении пользователя {telegram_id}: {e}')
        return False
    finally:
        cursor.close()

def get_all_users():
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT telegram_id FROM users')
        data = cursor.fetchall()
        return [row[0] for row in data]
    except Exception as e:
        logger.error(f'Ошибка при извлечении всех пользователей: {e}')
        return []
    finally:
        cursor.close()