#!/usr/bin/env python3
import sqlite3
from datetime import datetime
import uuid
import bcrypt

# Создаём подключение к БД
conn = sqlite3.connect('meetingmind.db')
cursor = conn.cursor()

# Хэшируем пароль
password = "test123456"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Генерируем UUID
user_id = str(uuid.uuid4())
now = datetime.now().isoformat()

# Проверяем, есть ли уже пользователь
cursor.execute("SELECT email FROM users WHERE email = 'test@test.com'")
if cursor.fetchone():
    print("⚠️ Пользователь test@test.com уже существует")
else:
    # Вставляем тестового пользователя
    cursor.execute("""
        INSERT INTO users (id, email, hashed_password, full_name, is_active, is_verified, created_at, updated_at)
        VALUES (?, ?, ?, 'Test User', 1, 1, ?, ?)
    """, (user_id, "test@test.com", hashed_password, now, now))
    
    conn.commit()
    print("✅ Пользователь создан!")
    print("")
    print("=" * 40)
    print("📧 Email: test@test.com")
    print("🔑 Пароль: test123456")
    print("=" * 40)

conn.close()
