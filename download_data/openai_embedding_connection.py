from openai import OpenAI
import logging
import json

class OpenAIEmbeddingConnecton:
    def __init__(self, openAIkey, embedding_model):
        """
        Initializes a connection to OpenAI using the specified API key and embedding model.
        """
        try:
            self.client = OpenAI(api_key=openAIkey)
            self.model = embedding_model
        except Exception as e:
            logging.error("Failed to initialize OpenAI client: %s", e)
            raise ConnectionError("Failed to connect to OpenAI with provided API key.")
            
    def get_embedding(self, text):
        """
        Retrieves an embedding for the given text using the configured model.
        """
        text = text.replace("\n", " ")
        try:
            response = self.client.embeddings.create(input=[text], model=self.model)
            return response.data[0].embedding
        except Exception as e:
            logging.error("Error getting embedding: %s", e)
            raise
