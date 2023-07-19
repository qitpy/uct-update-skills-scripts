import pymongo
import json
import time
import os

################
################ PLEASE CONFIG HERE ################
# mongodb://localhost:27017
# dbname: uctdev
database_uri = os.getenv("SCRIPT_DATABASE_URI")
database_dbname = os.getenv("SCRIPT_DATABASE_DBNAME")

################ PLEASE CONFIG HERE ################
################

# use pymongo to check connection to mongodb

# Create a MongoClient object
print("\nHope doing well! Connecting to MongoDB... 😈")
print("Checking connection to MongoDB...")
client = None
try:
    # The ismaster command is cheap and does not require authentication.
    client = pymongo.MongoClient(database_uri, serverSelectionTimeoutMS=5000)
    client.server_info()  # will throw an exception
    print("Connected to MongoDB successfully! 🤘")
    print(f"Database name: {database_dbname}")
except pymongo.errors.ConnectionFailure as e:
    print("\n❌ Failed to connect to MongoDB.\n")
    print(e._message)
    exit(1)

try:
    print()
    print(f"Starting to count documents to update...")
    # get processed_jobs_collection by name "processed_jobs"
    processed_jobs_collection = client[database_dbname]['processed_jobs']
    # get all documents from processed_jobs_collection
    query = {"processed_skills.ml_score": {"$eq": 0}}
    documents = processed_jobs_collection.find(query)
    editing_jobs_collection = client[database_dbname]['editing_jobs']
    # count documents to update
    docs_need_to_update_found = 0
    # print length of documents
    update_docs = []
    for doc in documents:
        update_docs.append(doc)
        docs_need_to_update_found += 1
    print(f"Total documents to update found in processed jobs: {docs_need_to_update_found}")
    time.sleep(1)
    print()

    # pending time before update:
    print("Pending time before update: 10 seconds")
    for i in range(10):
        print(f"Update after: {10-i} seconds")
        time.sleep(1)

    updated_count = 0
    # update documents
    print("Updating documents...")
    for index, doc in enumerate(update_docs):
        print()
        print(f"------------------------[{index}/{docs_need_to_update_found}] Updating In-Review Jobs Skills that have ml_score > 0: {doc['_id']}--------------------------")
        old_skills = [skill["_id"] for skill in doc['processed_skills']]
        # print json dumps
        print(f"** FROM: {json.dumps(old_skills, indent=4)}")

        new_skills = [skill["_id"] for skill in doc['processed_skills'] if skill["ml_score"] > 0]
        print(f"** TO: {json.dumps(new_skills, indent=4)}")

        # update document
        query = {"post_url": doc["post_url"], "status": {"$ne": "published"}}
        result = editing_jobs_collection.find_one_and_update(query, {"$set": {"skills": new_skills}})

        if result:
            updated_count += 1
        print(f"------------------------Done for: {doc['_id']}--------------------------")
        print()

        # TODO: clone dev to try

    print(f"Has {docs_need_to_update_found} in processed jobs, but just Updated {updated_count} documents that have not been published yet.")

except pymongo.errors.ConnectionFailure:
    print("Failed to connect to MongoDB.")
finally:
    # Close the client connection when you are done using it.
    client.close()
