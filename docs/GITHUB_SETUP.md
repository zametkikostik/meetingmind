# 📤 Загрузка на GitHub

## Шаг 1: Создайте репозиторий на GitHub

1. Откройте https://github.com/new
2. Введите имя репозитория: `meetingmind`
3. Выберите **Private** или **Public**
4. **НЕ** нажимайте "Initialize this repository with README"
5. Нажмите **Create repository**

## Шаг 2: Добавьте удалённый репозиторий

```bash
cd /home/kostik/meetingmind

# Замените YOUR_USERNAME на ваш username GitHub
git remote add origin https://github.com/YOUR_USERNAME/meetingmind.git

# Проверьте
git remote -v
```

## Шаг 3: Загрузите код на GitHub

```bash
# Отправить основную ветку
git push -u origin main

# Если используете SSH (рекомендуется):
# git remote set-url origin git@github.com:YOUR_USERNAME/meetingmind.git
# git push -u origin main
```

## Шаг 4: Проверьте загрузку

Откройте https://github.com/YOUR_USERNAME/meetingmind

Вы должны увидеть все файлы проекта.

---

## 🔐 Настройка SSH (рекомендуется)

### 1. Создайте SSH ключ
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 2. Добавьте ключ в GitHub
```bash
cat ~/.ssh/id_ed25519.pub
```

Скопируйте вывод и добавьте в:
GitHub → Settings → SSH and GPG keys → New SSH key

### 3. Переключите remote на SSH
```bash
git remote set-url origin git@github.com:YOUR_USERNAME/meetingmind.git
git push -u origin main
```

---

## 📋 .gitignore

Уже настроен и исключает:
- ✅ `.env` файлы (секреты)
- ✅ `.env.production` (продакшн секреты)
- ✅ `*.db`, `*.sqlite` (базы данных)
- ✅ `meetingmind.db` (локальная БД)
- ✅ `node_modules/`
- ✅ `venv/`
- ✅ `__pycache__/`
- ✅ `*.log`
- ✅ `docker/nginx/ssl/` (SSL сертификаты)

---

## 🏷️ Добавить тег версии

```bash
# Создать тег
git tag -a v1.0.0 -m "MeetingMind AI v1.0.0 - Initial release"

# Отправить теги на GitHub
git push origin --tags
```

---

## 📊 GitHub Actions (CI/CD)

Создайте файл `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd backend
        pytest

  test-frontend:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '20'
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    - name: Run tests
      run: |
        cd frontend
        npm test

  build-docker:
    runs-on: ubuntu-latest
    needs: [test-backend, test-frontend]
    steps:
    - uses: actions/checkout@v3
    - name: Build Docker images
      run: |
        docker-compose -f docker-compose.prod.yml build
```

---

## 📚 GitHub Pages (Documentation)

Для хостинга документации:

1. Откройте Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: /docs
4. Save

Документация будет доступна по адресу:
`https://YOUR_USERNAME.github.io/meetingmind/`

---

## 🎯 Следующие шаги

1. ✅ Создать репозиторий на GitHub
2. ✅ Добавить remote origin
3. ✅ Сделать git push
4. ⏳ Настроить GitHub Actions (CI/CD)
5. ⏳ Добавить GitHub Pages для документации
6. ⏳ Настроить automatic releases

---

## 📞 Помощь

Если возникли проблемы:

```bash
# Проверить статус
git status

# Проверить remote
git remote -v

# Пересоздать remote
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/meetingmind.git

# Принудительный push (осторожно!)
git push -f origin main
```
