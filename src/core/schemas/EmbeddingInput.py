from pydantic import BaseModel

class EmbeddingInput(BaseModel):
    input: str