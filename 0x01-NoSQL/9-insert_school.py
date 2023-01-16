#!/usr/bin/env python3
"""Inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs

    Args:
        mongo_collection (Document)
        kwargs (Dict): Key and value pairs attributes

    Return:
        (ObjectId) - Id of the data inserted
    """
    post_id = mongo_collection.insert_one(kwargs).inserted_id

    return post_id
