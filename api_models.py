from pydantic import BaseModel


class OutputModel(BaseModel):
    out_embed: str
    status: str
    model: str
