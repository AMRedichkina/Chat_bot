from neo4j import GraphDatabase
import logging
from neo4j_queries import create_summary, create_vector_index, check_index_exists, create_book_node

class Neo4jConnection:
    def __init__(self, uri, user, password):
        """
        Initializes a connection to a Neo4j database using the provided URI, username, and password.
        If the connection fails, it logs the error and raises an exception.
        
        Parameters:
        - uri (str): The URI of the Neo4j database.
        - user (str): The username for the Neo4j database.
        - password (str): The password for the Neo4j database.
        """
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            logging.error("Failed to connect to Neo4j: %s", e)
            raise

    def close(self):
        """
        Closes the connection to the Neo4j database. Logs that the connection has been closed.
        """
        self.driver.close()
        logging.info("Neo4j connection closed.")

    def load_book(self, genres, **book_data):
        """
        Loads a book into the Neo4j database. This includes creating nodes for the book, author, and genres,
        and setting up the appropriate relationships between them.
        If the operation fails, it logs the error and raises an exception.
        
        Parameters:
        - genres (list): A list of genres associated with the book.
        - book_data (dict): A dictionary containing the necessary book attributes 
        like title, author, language, rating, and publication year.
        """
        with self.driver.session() as session:
            try:
                session.execute_write(create_book_node, genres, **book_data)
            except Exception as e:
                logging.error("Failed to create book, author or genre nodes: %s", e)
                raise
        

    def load_summary(self, title, embeddings):
        """
        Attaches a vector property representing the book summary to an existing book node in the Neo4j database.
        If the operation fails, it logs the error and raises an exception.
        
        Parameters:
        - title (str): The title of the book.
        - embeddings (list): The embedding vector that represents the summary of the book.
        """
        with self.driver.session() as session:
            try:
                session.execute_write(create_summary, title, embeddings)
            except Exception as e:
                logging.error("Failed to create summary: %s", e)
                raise

    def check_index(self):
        """
        Checks if a vector index exists in the Neo4j database. Logs the result and returns a boolean indicating the presence of an index.
        If the check fails, it logs the error and raises an exception.
        
        Returns:
        - bool: True if the vector index exists, otherwise False.
        """
        with self.driver.session() as session:
            try:
                index_exists = session.execute_write(check_index_exists)
                if index_exists:
                    logging.info("Vector index already exists. No action taken.")
                    return True
                else:
                    logging.info("No vector index found.")
                    return False
            except Exception as e:
                logging.error("Failed to check index: %s", e)
                raise

    def create_index(self, vector_dimensions, similarity_function):
        """
        Creates a vector index for book summaries in the Neo4j database using the specified vector dimensions and similarity function.
        Logs the outcome of the operation.
        If the creation fails, it logs the error and raises an exception.
        
        Parameters:
        - vector_dimensions (int): The number of dimensions of the vector index.
        - similarity_function (str): The similarity function to use for the vector index.
        """
        with self.driver.session() as session:
            try:
                session.execute_write(create_vector_index, vector_dimensions, similarity_function)
                logging.info("Vector index created successfully.")
            except Exception as e:
                logging.error("Failed to create index: %s", e)
                raise
