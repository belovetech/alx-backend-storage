#!/usr/bin/env python3
"""List all documents in a collection"""


def list_all(mongo_collection):
    """List all documents in a collection

    Args
       mongo_collection (Document)
    """
    return mongo_collection.find()
