import streamlit as st
from llm import llm, embeddings
from graph import graph

from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain_core.prompts import ChatPromptTemplate

# Create an instance of Neo4jVector using an existing index.
neo4jvector = Neo4jVector.from_existing_index(
    embeddings,
    graph=graph,
    index_name="summaryPlots",
    node_label="Book",
    text_node_property="summary",
    embedding_node_property="plotEmbeddingSummury",
    retrieval_query="""
    
RETURN
    node.summary AS text,
    score,
    {
        book_title: node.title,
        author: [(book)-[:WRITTEN_BY]-(author) | author.name],
        genres: [(book)-[:HAS_GENRE]->(genre) | genre.name]
    } AS metadata
"""
)

# Convert the Neo4j vector search into a retriever that can be used in a chain.
retriever = neo4jvector.as_retriever()

# Template instructions for the chat prompt
instructions = (
    "Use the given context to answer the question."
    "If you don't know the answer, say you don't know."
    "Context: {context}"
)

# Create a chat prompt template from a series of system-human message pairs.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        ("human", "{input}"),
    ]
)

# Create a chain that combines document retrieval with an LLM for answering questions.
question_answer_chain = create_stuff_documents_chain(llm, prompt)
plot_retriever = create_retrieval_chain(
    retriever, 
    question_answer_chain
)

def get_movie_plot(input):
    """
    Retrieve movie plot summaries based on a given input query.

    Args:
        input (str): The input query for retrieving movie plot summaries.

    Returns:
        dict: The result from the retrieval chain, including plot summaries and associated metadata.
    """
    return plot_retriever.invoke({"input": input})
