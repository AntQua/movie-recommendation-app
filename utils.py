import weaviate
from weaviate.client import WeaviateClient
import os
from dotenv import load_dotenv

# Load environment variables from the `.env` file
load_dotenv()


def connect_to_my_db() -> WeaviateClient:
    """
    Helper function to connect to the Weaviate instance.
    To be used for data loading as well as queries.
    """

    client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("WEAVIATE_URL"),

        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_KEY")),

        # OpenAI API key for queries that require it
        headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")},
    )

    return client


def main():

    # Connect to Weaviate
    client = connect_to_my_db()

    try:
        # Check whether the client is ready
        assert client.is_ready()  # Check connection status (i.e. is the Weaviate server ready)

        # Try a query
        # movies = client.collections.get("Movie")
        # response = movies.query.near_text(query="time travel", limit=1)
        # assert len(response.objects) == 1
        print("Success! You appear to be correctly set up.")
    finally:
        # Close the connection
        client.close()


if __name__ == "__main__":
    main()
