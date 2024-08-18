import csv
from pinecone import Pinecone
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import time
import uuid

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_ALL_MINILM_L6_V2_INDEX")
custom_namespace='gptuesday'
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

print("BEFORE", index.describe_index_stats())

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

with open("./data/gptuesday_kb.csv") as kb_file:
    print(type(kb_file))

    csvreader = csv.reader(kb_file)

    header = next(csvreader)
    print(header)

    for row in csvreader:
        print('row')
        print('q:',row[0],'a:',row[1])

        embeddings = model.encode([row[0], row[1]])
        
        index.upsert(
          vectors=[
            # 1st index the question
            {
              # "id": hashlib.sha1(row[0].encode('utf-8')).hexdigest(),
              "id": str(uuid.uuid4()),
              "values": embeddings[0],
              "metadata": {
                  "q": row[0],
                  "a": row[1],
                  "created_at": int(time.time())   
              },
            },
            # 2nd index the answer
            {
              # "id": hashlib.sha1(row[1].encode('utf-8')).hexdigest(),
              "id": str(uuid.uuid4()),
              "values": embeddings[1],
              "metadata": {
                  "q": row[0],
                  "a": row[1],
                  "created_at": int(time.time())
              },
            },
          ],
          namespace=custom_namespace,
        )        

print('Record count AFTER adding knowledge ->', index.describe_index_stats())
