import utils
import weaviate.classes as wvc
from weaviate.util import generate_uuid5
import pandas as pd

client = utils.connect_to_my_db()  

movies = client.collections.get("Movie")
reviews = client.collections.get("Review")
synopses = client.collections.get("Synopsis")

movie_df = pd.read_csv("data/movies_data.csv")


# Import reviews data
review_objs = list()

# Iterate over the rows in the CSV file
for i, row in movie_df.iterrows():
    for c in [1, 2, 3]:  # There are three reviews per movie in this dataset
        col_name = f"Critic Review {c}"
        if len(row[col_name]) > 0:
            props = {
                "body": row[col_name],
            }
            review_uuid = generate_uuid5(row[col_name])
            data_obj = wvc.data.DataObject(properties=props, uuid=review_uuid)
            review_objs.append(data_obj)

response = reviews.data.insert_many(review_objs)

print(f"Insertion complete with {len(response.uuids)} objects.")
print(f"Insertion errors: {len(response.errors)}.")


# Import movies data
movie_objs = list()

# Iterate over the rows in the CSV file
for i, row in movie_df.iterrows():
    props = {
        "title": row["Movie Title"],
        "description": row["Description"],
        "rating": row["Star Rating"],
        "director": row["Director"],
        "movie_id": row["ID"],
        "year": row["Year"],
    }
    # Add references to reviews
    review_uuids = list()
    for c in [1, 2, 3]:
        col_name = f"Critic Review {c}"
        if len(row[col_name]) > 0:
            review_uuid = generate_uuid5(row[col_name])  # Identify the review IDs to refer to
            review_uuids.append(review_uuid)  # Collect the review IDs

    movie_uuid = generate_uuid5(row["ID"])
    data_obj = wvc.data.DataObject(
        properties=props,
        uuid=movie_uuid,
        references={"hasReview": review_uuids},
    )
    movie_objs.append(data_obj)

response = movies.data.insert_many(movie_objs)

print(f"Insertion complete with {len(response.uuids)} objects.")
print(f"Insertion errors: {len(response.errors)}.")



# Import synopses data
synopses_objs = list()

# Iterate over the rows in the CSV file
for i, row in movie_df.iterrows():

    # Create a dictionary of properties
    props = {
        "body": row["Synopsis"],
    }

    # Generate a UUID for the synopsis (use the same UUID as the movie)
    # Note: this is okay as the synopsis and movie are in different collections
    # Create a reference to the movie in the "forMovie" property
    movie_uuid = generate_uuid5(row["ID"])
    data_obj = wvc.data.DataObject(
        properties=props,
        uuid=movie_uuid,
        references={"forMovie": movie_uuid},
    )

    # Add the synopsis object to the list
    synopses_objs.append(data_obj)

# Insert the synopsis objects into the collection
response = synopses.data.insert_many(synopses_objs)

print(f"Insertion complete with {len(response.uuids)} objects.")
print(f"Insertion errors: {len(response.errors)}.")



# Add references from movies to synopses

# Create a list of references
synopses_refs = list()

# Iterate over the rows in the CSV file
for i, row in movie_df.iterrows():
    # Generate a UUID for the movie
    movie_uuid = generate_uuid5(row["ID"])

    # Create a reference object with the "hasSynopsis" property
    # Hint: use the "wvc.data.DataReference" class
    ref_obj = wvc.data.DataReference(
        from_property="hasSynopsis", from_uuid=movie_uuid, to_uuid=movie_uuid
    )

    # Add the reference object to the list
    synopses_refs.append(ref_obj)

# Add the references to the collection
response = movies.data.reference_add_many(synopses_refs)

print(f"Insertion complete with {len(synopses_refs)} objects.")
print(f"Insertion errors: {len(response.errors)}.")

client.close()
