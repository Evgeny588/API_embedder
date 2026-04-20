# Веб-сервис эмбеддингов.

**Использование**
1. Склонируйте репозиторий на компьютер: 
```bash 
git clone https://github.com/Evgeny588/API_embedder.git
```

2. Создайте в корне проекта файл ".env" и в нем создайте переменную MODEL = ...
3. Установите Poetry:
``` bash
curl -sSL https://install.python-poetry.org | python3 -
```
4. Установите флаг, чтобы файлы виртуального окружения были в репозитории:
``` bash
poetry config virtualenvs.in-project true
```
5. Установите зависимости:
``` bash
poetry install
```
6. Запустите сервер unicorn:
``` bash
uvicorn main:app
```
7. Откройте в браузере localhost (если uvicorn запускали без доп. аргументов)
8. В адресную строку после адреса localhost-a пропишите /docs - откроется интерфейс Swagger UI
9. Найдите метод *embedder/*
10. Поместите в папку inputs/ ваш текст в формате txt
11. В предложенный json в поле *text_or_filename* введите название файла, и нажмите *Execute*
12. Результат будет сохранен в папку *outputs/* в формате файла .txt с временной меткой в названии
13. Поддерживается возможность вставлять "сырой" текст прямо в json, в поле *text_or_filename*
