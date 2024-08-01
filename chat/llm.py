import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

def initialize_openai_services():
    """
    Initializes and returns OpenAI services for chat and embeddings.

    This function configures services using API keys and model information 
    retrieved from environment variables, encapsulating the initialization 
    logic to enhance modularity and reduce code duplication across your application.

    Returns:
        tuple: A tuple containing instances of ChatOpenAI and OpenAIEmbeddings.
    """
    # Retrieve OpenAI API key and model names from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chat_model = os.getenv("OPENAI_GEN_MODEL")
    embeddings_model = os.getenv("EMBEDDING_MODEL")

    # Initialize the OpenAI chat model
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model=chat_model,
    )

    # Initialize the OpenAI embeddings model
    embeddings = OpenAIEmbeddings(
        openai_api_key=openai_api_key,
        model=embeddings_model,
    )

    return llm, embeddings

# Get instances of OpenAI chat and embeddings services
llm, embeddings = initialize_openai_services()
