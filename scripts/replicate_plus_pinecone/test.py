from pinecone import Pinecone
import os
from dotenv import load_dotenv
import hashlib
import replicate
import time

load_dotenv()

print("REPLICATE_API_TOKEN", os.getenv("REPLICATE_API_TOKEN"))

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_IMAGEBIND_1024_DIMS_INDEX")
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

print("---> BEFORE <---", index.describe_index_stats())

# filename = "ADD.jpg"
# input = open(f"./data/media_assets/images_v1/{filename}", "rb")

print()

directory = "./data/media_assets/images_v1/"
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        print(os.path.join(directory, filename))

        input = open(f"./data/media_assets/images_v1/{filename}", "rb")

        output = replicate.run(
            "daanelson/imagebind:0383f62e173dc821ec52663ed22a076d9c970549c209666ac3db181618b7a304",
            input={
                # vvv TEXT EXAMPLE vvv
                # "modality": "text",
                # "text_input": "An astronaut riding a horse on mars, trending on artstation, 4k, good anatomy"
                # ^^^ ^^^ ^^^
                # vvv IMAGE EXAMPLE vvv
                "modality": "vision",
                "input": input
                # ^^^ ^^^ ^^^
            }
        )

        print(len(output))

        index.upsert(
          vectors=[
            {
              "id": hashlib.sha1(filename.encode('utf-8')).hexdigest(),
              "values": output,
              "metadata": {
                  "modality": "vision",
                  "filename": filename,
                  "created_at": int(time.time())}
            },
          ],
          namespace='media_assets'
        )

# print("AFTER", index.describe_index_stats())