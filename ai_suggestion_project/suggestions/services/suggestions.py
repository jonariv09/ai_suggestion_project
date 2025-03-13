import os
import json
import faiss
import math
import numpy as np
import pandas as pd
from django.conf import settings
from sentence_transformers import SentenceTransformer

selected_columns = ['type','title','director','cast','release_year','listed_in','description']

class SuggestionService:
  def __init__(self):
    # Declaracion del modelo
    self.model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Conversion del dataset a json
    json_path = os.path.join(settings.BASE_DIR, "ai_suggestion_project", "dataset", "clean_netflix_titles.json")

    self.df_json = pd.read_json(json_path, lines=True).to_dict(orient='records')
    
    index_path = os.path.join(settings.BASE_DIR, "ai_suggestion_project", "dataset", "faiss_index")
    
    if os.path.exists(index_path):
      # Lectura del indice
      self.index = faiss.read_index(index_path)
  
  def create_suggestions(self, request_movie):    
    ## Generate embedding for request_movie
    embedding_request_movie = np.array([self.model.encode(json.dumps(request_movie))])

    ## Based on the request movie get the 5 suggestions
    D, I = self.index.search(embedding_request_movie, 5)

    best_matches = np.array(self.df_json)[I.flatten()]

    return best_matches