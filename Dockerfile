# Устанавливаем зависимости вашего приложения
FROM python:3.9-slim

COPY requirements.txt /app/requirements.txt
# Устанавливаем зависимости вашего приложения
RUN apt-get update && apt-get install -y python3-pip bash && \
    pip install --no-cache-dir -r /app/requirements.txt

# Копируем файлы вашего приложения в контейнер
COPY . /app
# Устанавливаем рабочую директорию
WORKDIR /app

# Запускаем ваше приложение
CMD ["python", "tgbot.py"]