import streamlit as st
from llm import llm, embeddings
from graph import graph

from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain_core.prompts import ChatPromptTemplate

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
        author: [(node)-[:WRITTEN_BY]-(author) | author.name]
    } AS metadata
"""
)

retriever = neo4jvector.as_retriever()

instructions = (
    "Use the given context to answer the question."
    "If you don't know the answer, say you don't know."
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
plot_retriever = create_retrieval_chain(
    retriever, 
    question_answer_chain
)

def get_book_plot(input):
    """
    Retrieve book plot summaries based on a given input query.

    Args:
        input (str): The input query for retrieving book plot summaries.

    Returns:
        dict: The result from the retrieval chain, including plot summaries and associated metadata.
    """
    return plot_retriever.invoke({"input": input})
