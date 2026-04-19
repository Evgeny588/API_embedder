from pydantic import BaseModel


class InputModel(BaseModel):
    text_or_filename: str | None = None


class OutputModel(BaseModel):
    out_embed: str
    status: str
    model: str
