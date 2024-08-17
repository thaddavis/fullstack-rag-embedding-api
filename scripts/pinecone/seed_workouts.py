import csv
from pinecone import Pinecone
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import time
import hashlib
import psycopg

load_dotenv()

conn_info = os.getenv("POSTGRES_URL")
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_ALL_MINILM_L6_V2_INDEX")
custom_namespace='workouts'
# created_by = "tad@cmdlabs.io"
created_by = "arnold@fit.ai"
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

with open("./data/workouts.csv") as kb_file:
    print(type(kb_file))

    csvreader = csv.reader(kb_file)

    header = next(csvreader)
    print(header)

    for row in csvreader:
        print('row')
        print('title:',row[0],'description:',row[1])

        # vvv DEPRECATED vvv
        # conn = psycopg.connect(conn_info) # Connect to PostgreSQL
        # cursor = conn.cursor() # Create a cursor object
        # query = "INSERT INTO workouts (user_id, name, description) VALUES (%s, %s, %s)" # Define the SQL query
        # cursor.execute(query, (4, row[0], row[1])) # Execute the query for each row in the CSV file
        # conn.commit() # Commit the changes to the database
        # cursor.close() # Close the cursor
        # conn.close() # Close the connection
        # ^^^ DEPRECATED ^^^

        # vvv Use Pinecone to upsert the embeddings vvv

        embeddings = model.encode([row[0], row[1]])
        
        index.upsert(
          vectors=[
            # 1st index the title of the workout
            {
              "id": hashlib.sha1(row[0].encode('utf-8')).hexdigest(),
              "values": embeddings[0],
              "metadata": {
                  "title": row[0],
                  "description": row[1],
                  "created_at": int(time.time()),
                  "created_by": "arnold@fit.ai",
                  "uuid": hashlib.sha1(row[0].encode('utf-8')).hexdigest()
              },
            },
            # 2nd index the description of the workout
            {
              "id": hashlib.sha1(row[1].encode('utf-8')).hexdigest(),
              "values": embeddings[1],
              "metadata": {
                  "title": row[0],
                  "description": row[1],
                  "created_at": int(time.time()),
                  "created_by": "arnold@fit.ai",
                  "uuid": hashlib.sha1(row[0].encode('utf-8')).hexdigest()
              },
            },
          ],
          namespace=custom_namespace,
        )  

print('Record count AFTER adding knowledge ->', index.describe_index_stats())




