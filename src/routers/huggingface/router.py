from fastapi import APIRouter, Response
from sentence_transformers import SentenceTransformer

from core.schemas.EmbeddingInput import EmbeddingInput

router = APIRouter(
    prefix='/huggingface',
    tags=['huggingface']
)

@router.post("/embedding")
def create_embeddings(response: Response, textToEmbed: EmbeddingInput):
    
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = embedding_model.encode(textToEmbed.input)
    embeddings_list = embeddings.tolist()
    
    return {"embedding": embeddings_list, "model": "sentence-transformers/all-MiniLM-L6-v2"}