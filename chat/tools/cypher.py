import streamlit as st
from llm import llm
from graph import graph
from langchain.prompts import PromptTemplate

from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain

CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about books and provide recommendations based on a specific schema. Convert the user's question into an appropriate Cypher query.

Instructions:
- Use only the provided node types and their properties.
- Handle author names and genre names with the correct case sensitivity as stored in the database.
- Provide examples for queries like:
  1. Find books by a specific author.name only:
  ```
  MATCH (b)-[r:WRITTEN_BY]->(a: {{name: "Author Name"}})
  RETURN b.title, b.publication_year, b.rating
  ```
  2. If you're looking for similar books in the same genre:
  ```
  MATCH (b:Book {{title: "Book name"}})-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(b2:Book)
  RETURN b2.title, b2.publication_year, b2.rating, b2.summary
  ```
  3. Find detailed information about a specific book.name:
  ```
  MATCH (b: {{title:"Book name"}})-[r:WRITTEN_BY]->(a)
  MATCH (b)-[r:HAS_GENRE]->(g)
  RETURN b.title, b.publication_year, b.rating, b.summary, a.name, g.name
  ```
  4. Find books of a specific genre with high book.rating:
  ```
  MATCH (b:Book)-[:HAS_GENRE]->(g:Genre {{name: "Genre Name"}})
  WHERE b.rating >= 4.0
  RETURN b.title, b.publication_year, b.rating
  ORDER BY b.rating DESC
  LIMIT 10
  ```
  5. Find books by other authors but in the same genre.name:
  ```
  MATCH (a1:Author)-[:WRITTEN_BY]-(b:Book)-[:HAS_GENRE]-(g:Genre)-[:HAS_GENRE]-(b2:Book)-[:WRITTEN_BY]-(a2:Author)
  WHERE a1.name <> a2.name
  RETURN a1.name, a2.name, collect(g.name) AS shared_genres, count(g) AS genre_count
  ORDER BY genre_count DESC
  LIMIT 5
  ```

Schema: {schema}

Question: {question}
"""

cypher_generation_prompt = PromptTemplate(
    template=CYPHER_GENERATION_TEMPLATE,
    input_variables=["schema", "question"],
)

cypher_qa = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    cypher_prompt=cypher_generation_prompt,
    verbose=True
)
