import os
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, UploadFile, Form, File
from contextlib import asynccontextmanager

from modules import init_model, clear_memory, write_embedding 
from set_logging import setup_logging
from api_models import OutputModel

logger = setup_logging(__name__)
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"App started in {datetime.now()}.")
    app.state.model = init_model(model=os.getenv("MODEL"))
    logger.info(f"Model {os.getenv('MODEL')} ready.")

    yield

    clear_memory()
    logger.info("Recources cleared")


app = FastAPI(lifespan=lifespan)


@app.get("/status")
async def status() -> dict:
    return {"status": "ok"}


@app.post("/embedder", response_model=OutputModel)
async def get_embedding(
    request: Request,
    text: Optional[str] = Form(None, description="Сырой текст для эмбеддинга"),
    file: Optional[UploadFile] = File(None, description="Файл .txt или .json")
):
    """
    Принимает либо сырой текст, либо загруженный файл.
    Возвращает путь к сохраненному эмбеддингу.
    """
    model = request.app.state.model
    text_to_embed = ""

    if not text and not file:
        raise HTTPException(
            status_code=400,
            detail="Пожалуйста, передайте текст в поле 'text' или загрузите файл в поле 'file'."
        )
    
    if text and file:
        raise HTTPException(
            status_code=400,
            detail="Выберите что-то одно: либо текстовое поле, либо загрузку файла."
        )

    if file:
        filename = file.filename.lower()
        if not (filename.endswith('.txt') or filename.endswith('.json')):
            raise HTTPException(
                status_code=400, 
                detail="Разрешены только файлы с расширением .txt или .json"
            )
        
        try:
            logger.info(f"Получен файл: {file.filename}. Чтение содержимого...") 
            content_bytes = await file.read()
            text_to_embed = content_bytes.decode("utf-8")
        except Exception as e:
            logger.error(f"Ошибка чтения файла: {e}")
            raise HTTPException(status_code=400, detail="Не удалось прочитать или декодировать файл.") 

    elif text:
        text_to_embed = text

    if not text_to_embed.strip():
        raise HTTPException(status_code=400, detail="Текст для эмбеддинга пуст.")
 
    try:
        embeddings = list(model.embed([text_to_embed]))
        
        filepath = write_embedding(embeddings[0])

        return {
            "out_embed": str(filepath),
            "status": "ok",
            "model": os.getenv("MODEL", "jinaai/jina-embeddings-v3"),
        }
    except Exception as e:
        logger.exception(f"Ошибка при создании эмбеддинга: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Внутренняя ошибка сервера при обработке модели."
        )


@app.get("/models")
async def get_supported_models():
    from fastembed import TextEmbedding

    return TextEmbedding.list_supported_models()
