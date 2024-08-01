def parse_embeddings(row):
    """
    Parses the 'Embeddings' field from a CSV row into a list of floats.
    """
    embeddings = row['Embeddings'].strip("[]").split(',')
    return list(map(float, embeddings))

def parse_genres(genres):
    """
    Splits and standardizes the genre data from a CSV string into individual genres.
    """
    standardized = genres.replace('/', ',')
    return [part.strip() for part in standardized.split(',')]
