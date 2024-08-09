from fastapi import APIRouter, Response
from sentence_transformers import SentenceTransformer

router = APIRouter(
    prefix='/huggingface',
    tags=['huggingface']
)

@router.post("/embedding")
def create_embeddings(response: Response, text: list[str]):
    
    embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = embedding_model.encode(text[0]) # [0] HACK BUT IT WORKS
    embeddings_list = embeddings.tolist()
    
    return {"embedding": embeddings_list, "model": "sentence-transformers/all-MiniLM-L6-v2"}