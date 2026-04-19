from pydantic import BaseModel
from typing import Optional


class InputModel(BaseModel):
    text: Optional[str] = None


class OutputModel(BaseModel):
    out_embed: str
    status: str
