# TLDR

Self-hosted Embeddings API for "Fullstack Vectors" course

## How to run the FastAPI

- pip install -r requirements.txt
- uvicorn src.main:app --host 0.0.0.0 --port 7000 --proxy-headers --reload

## How to save versions of top-level packages

- pip install pipreqs
- pipreqs . --force

## Example cURL POST command for testing embeddings generation

```
curl -X POST http://localhost:7000/huggingface/embedding \
     -H "Content-Type: application/json" \
     -d '{"input": "hello world"}'
```

## Hugging Face reference links

- https://www.sbert.net/docs/sentence_transformer/pretrained_models.html#original-models
- https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 (384 dimensional vectors)