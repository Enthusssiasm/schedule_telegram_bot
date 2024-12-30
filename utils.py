import random
import string

def generate_password(length=8):
    """Генерирует случайный пароль из букв и цифр заданной длины."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))