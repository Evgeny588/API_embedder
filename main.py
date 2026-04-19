import os
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager

from modules import init_model, clear_memory, write_embedding, file_read
from set_logging import setup_logging
from api_models import InputModel, OutputModel

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
async def get_embedding(inputs: InputModel, request: Request) -> dict:
    """Get embedding from raw text or file"""
    input_data = inputs.text_or_filename
    model = request.app.state.model

    if input_data:
        is_file = input_data.lower().endswith((".txt", ".json"))

        if is_file:
            logger.info(f"Detected file path: {input_data}. Reading file...")
            text_to_embed = await file_read(input_data)
        else:
            text_to_embed = input_data

        try:
            embeddings = list(model.embed([text_to_embed]))

            filepath = write_embedding(embeddings[0])

            return {
                "out_embed": str(filepath),
                "status": "ok",
                "model": str(os.getenv("MODEL")),
            }
        except Exception as e:
            logger.exception(f"Embedding error: {str(e)}")
            raise HTTPException(
                status_code=500, detail="Internal server error during processing"
            )

    raise HTTPException(
        status_code=400,
        detail="Input text is empty. Please provide raw text or a path to .txt/.json file",
    )


@app.get("/models")
async def get_supported_models():
    from fastembed import TextEmbedding

    return TextEmbedding.list_supported_models()
