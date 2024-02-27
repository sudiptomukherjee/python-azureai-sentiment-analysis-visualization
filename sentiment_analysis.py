from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import dotenv_values
import os

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
env_vars = dotenv_values(env_path)

# Azure Text Analytics credentials
key = env_vars.get("KEY")
endpoint = env_vars.get("ENDPOINT")
# Check if the key is None
if key is None:
    raise ValueError("Key for AzureAI service was not foind")

def chunk_text(text):
    max_chunk_size = 5120
    chunks = []
    for i in range(0, len(text), max_chunk_size):
        chunks.append(text[i:i + max_chunk_size])
    return chunks

def analyze_sentiment_azure(texts):
    # Initialize Azure Text Analytics client
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Analyze sentiment for each batch of text chunks
    sentiment_scores = []
    for text in texts:
        text_chunks = chunk_text(text)
        for chunk in text_chunks:
            response = text_analytics_client.analyze_sentiment([chunk])
            for doc in response:
                if not doc.is_error:
                    sentiment_scores.append(doc.sentiment)
                else:
                    print(f"Error processing document: {doc.id}, Error: {doc.error}")
                    sentiment_scores.append(None)  # Append None for error documents

    return sentiment_scores
