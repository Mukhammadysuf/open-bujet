# OpenBudget Telegram Bot

Telegram бот для голосования и связи с админом.  
Разработан на Python + python-telegram-bot.

## 🚀 Деплой на Render
1. Создать репозиторий на GitHub и загрузить файлы проекта.
2. На https://render.com создать новый Web Service и подключить репозиторий.
3. Указать Build Command:
   ```
   pip install -r requirements.txt
   ```
4. Указать Start Command:
   ```
   python bot.py
   ```
5. В Settings → Environment Variables добавить:
   ```
   TOKEN=<твой_токен>
   ```
6. Нажать Deploy 🎉
