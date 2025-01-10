import utils
import weaviate.classes as wvc

# Connect to the weaviate database
client = utils.connect_to_my_db()  

# Delete any previously created collections with the same name
client.collections.delete("Movie")
client.collections.delete("Review")
client.collections.delete("Synopsis")

# Add collection for reviews
reviews = client.collections.create(
    # Set the name of the collection
    name="Review",

    # Set modules to be used
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),    # Set the vectorizer
    #generative_config=wvc.config.Configure.Generative.openai(),             # Set the generative model
    # Could also explicitly set the model, e.g.:
    generative_config=wvc.config.Configure.Generative.openai(model="gpt-4-1106-preview"),

    # Define the properties of the collection
    properties=[
        wvc.config.Property(
            name="body",  # Set the name of the property
            data_type=wvc.config.DataType.TEXT,  # Set the data type of the property
        ),
    ],
)

# Add collection for movies
movies = client.collections.create(
    # Set the name of the collection
    name="Movie",

    # Set modules to be used
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),    # Set the vectorizer module
    generative_config=wvc.config.Configure.Generative.openai(),             # Set the generative module

    # Define the properties of the collection
    properties=[
        wvc.config.Property(
            # Set the name of the property
            name="title",
            # Set the data type of the property
            data_type=wvc.config.DataType.TEXT,
        ),
        wvc.config.Property(
            name="description",
            data_type=wvc.config.DataType.TEXT,
        ),
        wvc.config.Property(
            name="movie_id",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="year",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="rating",
            data_type=wvc.config.DataType.NUMBER,
        ),
        wvc.config.Property(
            name="director",
            data_type=wvc.config.DataType.TEXT,
            skip_vectorization=True,
        ),
    ],
    # Set reference properties
    references=[
        wvc.config.ReferenceProperty(
            name="hasReview",           # Set the name of the reference property
            target_collection="Review", # Set the name of the target collection
        )
    ],
)


# Add a collection for synopses
synopses = client.collections.create(
    name="Synopsis",
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
    generative_config=wvc.config.Configure.Generative.openai(model="gpt-4-1106-preview"),
    properties=[
        wvc.config.Property(
            name="body",
            data_type=wvc.config.DataType.TEXT,
        ),
    ],
    # A reference property with name "forMovie". Points to the "Movie" collection
    references=[
        wvc.config.ReferenceProperty(
            name="forMovie",
            target_collection="Movie",
        )
    ],
)


# Add a reference property to the "Movie" collection with name "hasSynopsis".
# This points to the "Synopsis" collection
movies.config.add_reference(
    wvc.config.ReferenceProperty(
        name="hasSynopsis",
        target_collection="Synopsis"
    )
)

client.close()
