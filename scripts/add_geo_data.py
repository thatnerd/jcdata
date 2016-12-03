#!/usr/bin/env python
"""
Takes water data from the DB, uses street address to get geo loc from google.

Usage:
    ./add_geo_data.py [options]

Options:
    -h --help               Show this text.
    --port <port>           Port that mongod is listening on [default: 27017]
    --host <hostname>       Hostname where mongod lives [default: localhost]
    --dbname <dbname>       Name of the database with the data [default: jc]
    --collname <collname>   Collection in the db with the data
                                [default: sewerMaintenance]
"""

from docopt import docopt
import pymongo
import time


def get_documents(collection):
    """
    Captures all documents in the collection.
    """
    curs = collection.find()
    return curs


def get_addresses(doc):
    """
    Returns a smaller doc with just the _id, Address, and Street fields.
    """
    fields = ['_id', 'Address', 'Street']
    new_doc = {field: doc[field] for field in fields}
    return new_doc

def add_geodata_to_doc(doc, collection, geo_data):
    """
    Updates doc in the database to include geo data.

    Inputs
    ------

    doc (dict): contains _id field used in the db
    collection (MongoClient.database.collection object): Queryable collection
        object
    geo_data (dict): geo data to add to the database. It will use the following
        schema:
            {
               location: {
                  type: "Point",
                  coordinates: [<longitude>, <latitude>]
               },
               name: "<name>"
            }
    """
    _id = doc['_id']
    try:
        collection.update_one({'_id': _id}, {'$set': {'geodata': geo_data}})
    except Exception as e:
        print("Unexpected exception: {e}".format(e=e))
        return False
    return True


def main():
    opts = docopt(__doc__)
    hostname = opts['--host']
    port = int(opts['--port'])
    dbname = opts['--dbname']
    collname = opts['--collname']
    client = pymongo.MongoClient(host=hostname, port=port)
    db = client[dbname]
    collection = db[collname]
    curs = get_documents(collection)
    for doc in curs:
        print get_addresses(doc)


if __name__ == '__main__':
    main()
