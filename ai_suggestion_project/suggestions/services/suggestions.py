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

    # importacion del dataset
    csv_path = os.path.join(settings.BASE_DIR, "ai_suggestion_project", "dataset", "netflix_titles.csv")
    
    self.df = pd.read_csv(csv_path).fillna(0)[selected_columns]
    
    # Conversion del dataset a json
    json_path = os.path.join(settings.BASE_DIR, "ai_suggestion_project", "dataset", "clean_netflix_titles.json")
    if not os.path.exists(json_path):
      self.df.to_json(json_path, lines=True, orient='records')

    self.df_json = pd.read_json(json_path, lines=True)
    self.df_json = self.df_json.to_dict(orient='records')
    # print(self.df_json)
    print(self.df_json)

    # Guardar representación JSON de los registros
    # self.df['json_representation'] = np.vectorize(self.create_json_representation)(self.df["type"],
    #                                                                                self.df["title"],
    #                                                                                self.df["director"],
    #                                                                                self.df["cast"],
    #                                                                                self.df["release_year"],
    #                                                                                self.df["listed_in"],
    #                                                                                self.df["description"],
    #                                                                               )
    
    # print(self.df['json_representation'].values)
    
    # Cargar o generar embeddings
    embeddings_path = os.path.join(settings.BASE_DIR, "ai_suggestion_project", "dataset", "embeddings.npy")
    index_path = os.path.join(settings.BASE_DIR, "ai_suggestion_project", "dataset", "faiss_index")

    if os.path.exists(embeddings_path) and os.path.exists(index_path):
      self.embeddings = np.load(embeddings_path)
      self.index = faiss.read_index(index_path)
    else:
      self.embeddings = np.array([self.model.encode(json.dumps(entry)) for entry in self.df_json])
      np.save(embeddings_path, self.embeddings)  # Guardar embeddings

      self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
      self.index.add(self.embeddings)
      faiss.write_index(self.index, index_path)  # Guardar índice FAISS

  def create_json_representation(self, type,title,director,cast,release_year,listed_in,description):
    return {
      'type': type,
      'title': title,
      'director': director,
      'cast': cast,
      'release_year': release_year,
      'listed_in': listed_in,
      'description': description
    }
    
  def clean_value(self, x):
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None  # O puedes usar otro valor, como 0
    return x
  
  def create_suggestions(self, request_movie):    
    # self.df['json_representation'] = self.df.apply(self.create_json_representation, axis=1)
    # self.df['json_representation'] = np.vectorize(self.create_json_representation)(self.df["type"],
    #                                                                                self.df["title"],
    #                                                                                self.df["director"],
    #                                                                                self.df["cast"],
    #                                                                                self.df["release_year"],
    #                                                                                self.df["listed_in"],
    #                                                                                self.df["description"],
    #                                                                               )
    
    # embeddings = np.array([model.encode(json.dumps(entry)) for entry in self.df['json_representation'].values])
    # index = faiss.IndexFlatL2(embeddings.shape[1])
    # index.add(embeddings)
    
    ## Generate embedding for request_movie
    embedding_request_movie = np.array([self.model.encode(json.dumps(request_movie))])
    
    ## Based on the request movie get the 5 suggestions
    D, I = self.index.search(embedding_request_movie, 5)
    
    best_matches = np.array(self.df_json)[I.flatten()]
    
    return best_matches