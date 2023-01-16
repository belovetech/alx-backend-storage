#!/usr/bin/env python3
"""List of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of school having a specific topic

    Args:
       mongo_collection (Document): pymongo collection object
       topic (str): topic to search for
    """
    return mongo_collection.find({"topics": topic})
