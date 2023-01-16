#!/usr/bin/env python3
"""Changes all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """Changes all topics of a school document based on the name

    Args:
        mongo_collection (Document): pymongo collection object
        name (str): school name to update
        topics (List[str]): list of topics offered in the school
    """
    query = {"name": name}
    newvalue = {"$set": {"topics": topics}}

    mongo_collection.update_many(query, newvalue)
