from pinecone import Pinecone
import os
from dotenv import load_dotenv
import hashlib
import replicate
import time

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_IMAGEBIND_1024_DIMS_INDEX")
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

print("---> BEFORE <---", index.describe_index_stats())

directory = "./data/media_assets"
for filename in os.listdir(directory):
    if filename.endswith(".wav"):
        print(os.path.join(directory, filename))
        input = open(f"./data/media_assets/audio_v1/{filename}", "rb")
        vector = replicate.run(
            "daanelson/imagebind:0383f62e173dc821ec52663ed22a076d9c970549c209666ac3db181618b7a304",
            input={
                "modality": "audio",
                "input": input
            }
        )
        index.upsert(
          vectors=[
            {
              "id": hashlib.sha1(filename.encode('utf-8')).hexdigest(),
              "values": vector,
              "metadata": {
                "modality": "audio",
                "filename": filename,
                "created_at": int(time.time())
              }
            },
          ],
          namespace='media_assets'
        )
    elif filename.endswith(".jpg") or filename.endswith(".png"):
        print(os.path.join(directory, filename))
        input = open(f"./data/media_assets/images_v1/{filename}", "rb")
        vector = replicate.run(
            "daanelson/imagebind:0383f62e173dc821ec52663ed22a076d9c970549c209666ac3db181618b7a304",
            input={
                "modality": "vision",
                "input": input
            }
        )
        index.upsert(
          vectors=[
            {
              "id": hashlib.sha1(filename.encode('utf-8')).hexdigest(),
              "values": vector,
              "metadata": {
                "modality": "vision",
                "filename": filename,
                "created_at": int(time.time())
              }
            },
          ],
          namespace='media_assets'
        )
      
print("AFTER", index.describe_index_stats())