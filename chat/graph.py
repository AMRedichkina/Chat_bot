import os
from langchain_community.graphs import Neo4jGraph

def create_neo4j_graph():
    """
    Creates and returns a Neo4jGraph object configured with credentials
    retrieved from environment variables.

    This function is particularly useful for setting up connections
    to a Neo4j database by abstracting away the details of reading
    environment variables and handling connections directly within
    other parts of your codebase.

    Returns:
        Neo4jGraph: An instance of Neo4jGraph connected to the specified Neo4j database.
    """
    # Retrieve database connection details from environment variables
    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    # Create and return a Neo4jGraph object
    return Neo4jGraph(url=url, username=username, password=password)

# Instantiate the Neo4j graph using the function defined above
graph = create_neo4j_graph()
