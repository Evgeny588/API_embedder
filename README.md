# API Embedder

Сервис генерации эмбеддингов.

## 1. Сборка и запуск в Docker

Сборка Docker-образа:
```bash
docker build -t api_embedder .
```

Запуск контейнера с сохранением кэша моделей на хосте:
```bash
docker run -d -p 8000:8000 -v \$(pwd)/cache_models:/api_embedder/cache_models --name embedder api_embedder
```

## 2. Локальный запуск (в виртуальном окружении)

Установка зависимостей:
```bash
pip install -r requirements.txt
```

Запуск сервера разработки:
```bash
uvicorn main:app 
```

## 3. Примеры запросов (API)

Интерактивная документация: http://localhost:8000/docs

Отправка текста:
```bash
curl -X POST "http://localhost:8000/embedder" -F "text=Пример текста"
```

Отправка файла:
```bash
curl -X POST "http://localhost:8000/embedder" -F "file=@document.txt"
```

## 4. Структура директорий

* `cache_models/` — Кэш весов нейросети (монтируется извне).
* `outputs/` — Директория выходных ответов в .txt формате
* `logs/` — Логи приложения.

