import os
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager

from modules import init_model, clear_memory, write_embedding
from set_logging import setup_logging
from api_models import InputModel, OutputModel

logger = setup_logging(__name__)
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"App started in {datetime.now()}.")
    app.state.model = init_model(model=os.getenv("MODEL"))
    logger.info("Model ready.")

    yield

    clear_memory()
    logger.info("Recources cleared")


app = FastAPI(lifespan=lifespan)


@app.get("/status")
async def status() -> dict:
    return {"status": "ok"}


@app.post("/embedder", response_model=OutputModel)
async def get_embedding(inputs: InputModel, request: Request) -> dict:
    """Get embedding"""
    text = inputs.text
    model = request.app.state.model

    if text is not None:
        try:
            embeddings = list(model.embed([text]))
            filepath = write_embedding(embeddings[0])

            return {"out_embed": f"{filepath}", "status": "ok"}
        except Exception as e:
            logger.exception(f"Exception: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    else:
        raise HTTPException(
            status_code=400, detail="Empty input, please enter text in inputs/input.txt"
        )
