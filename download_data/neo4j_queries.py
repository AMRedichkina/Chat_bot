def create_book_node(tx, genres, **book_data):
    """
    Creates a book node and its relationships in the Neo4j database.
    This function uses the MERGE statement to ensure that duplicates are not created.
    It sets up relationships between the Book node and Author, and Genre nodes.
    
    Parameters:
    - tx (Transaction): The Neo4j transaction.
    - genres (list): A list of genres associated with the book.
    - book_data (dict): A dictionary containing book attributes such as title, author, language, rating, and publication year.
    """
    query = """
    MERGE (b:Book {title: $title})
    SET b += {language: $lang, rating: $rating, publication_year: $year, summary: $summary}
    MERGE (a:Author {name: $author})
    MERGE (b)-[:WRITTEN_BY]->(a)
    WITH b
    UNWIND $genres as genreName
        MERGE (g:Genre {name: genreName})
        MERGE (b)-[:HAS_GENRE]->(g)
    """
    tx.run(query, genres=genres, **book_data)

def create_summary(tx, title, embeddings):
    """
    Attaches a vector property for text embeddings to an existing book node in the Neo4j database.
    This function is intended for storing embeddings that represent the plot summary.
    
    Parameters:
    - tx (Transaction): The Neo4j transaction.
    - title (str): The title of the book, used to merge the book node.
    - embeddings (list): The embedding vector representing the book's summary.
    """
    query = """
    MERGE (b:Book {title: $title})
    WITH b
    CALL db.create.setNodeVectorProperty(b, 'plotEmbeddingSummury', $embeddings)
    """
    tx.run(query, title=title, embeddings=embeddings)

def check_index_exists(tx):
    """
    Checks if a vector index exists in the database.
    This function queries the database to see if there's an existing vector index on book summaries.
    
    Parameters:
    - tx (Transaction): The Neo4j transaction.
    
    Returns:
    - bool: True if the index exists, False otherwise.
    """
    query = """
    SHOW INDEXES YIELD id, name, type, state, populationPercent WHERE type = "VECTOR"
    """
    result = tx.run(query)
    return result.single() is not None

def create_vector_index(tx, vector_dimensions, similarity_function):
    """
    Creates a vector index on book summary embeddings in the Neo4j database.
    The index is configured based on specified dimensions and similarity function.
    It enhances the performance of similarity searches based on vector properties.
    
    Parameters:
    - tx (Transaction): The Neo4j transaction.
    - vector_dimensions (int): The number of dimensions of the vector index.
    - similarity_function (str): The similarity function to use for the vector index.
    """
    
    query = """
    CREATE VECTOR INDEX summaryPlots IF NOT EXISTS
    FOR (b:Book)
    ON b.plotEmbeddingSummury
    OPTIONS {indexConfig: {
     `vector.dimensions`: $vector_dimensions,
     `vector.similarity_function`: $similarity_function
    }}
    """
    tx.run(query, vector_dimensions=vector_dimensions, similarity_function=similarity_function)

