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


def main():
    opts = docopt(__doc__)



if __name__ == '__main__':
    main()
