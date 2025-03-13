#!/usr/bin/env python3

import os
import json
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

selected_columns = ['type','title','director','cast','release_year','listed_in','description']

def main():
  # Declaracion del modelo
  model = SentenceTransformer("all-MiniLM-L6-v2")

  # importacion del dataset
  csv_path = os.path.join(BASE_DIR, "ai_suggestion_project", "dataset", "netflix_titles.csv")
  
  df = pd.read_csv(csv_path).fillna(0)[selected_columns]
  
  # Conversion del dataset a json
  json_path = os.path.join(BASE_DIR, "ai_suggestion_project", "dataset", "clean_netflix_titles.json")
  if not os.path.exists(json_path):
    df.to_json(json_path, lines=True, orient='records')

  df_json = pd.read_json(json_path, lines=True)
  df_json = df_json.to_dict(orient='records')

  # Cargar o generar embeddings
  embeddings_path = os.path.join(BASE_DIR, "ai_suggestion_project", "dataset", "embeddings.npy")
  index_path = os.path.join(BASE_DIR, "ai_suggestion_project", "dataset", "faiss_index")

  if os.path.exists(embeddings_path) and os.path.exists(index_path):
    print("Embeddings and FAISS Index files existent")
  else:
    embeddings = np.array([model.encode(json.dumps(entry)) for entry in df_json])
    np.save(embeddings_path, embeddings)  # Guardar embeddings

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, index_path)  # Guardar índice FAISS

main()