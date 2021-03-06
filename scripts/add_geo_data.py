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
    --addAddress            Whether or not to add the 'addressString' field to
                                all documents [default: False].
"""

from docopt import docopt
import pymongo
import time
import geocode

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


def add_geodata(doc, collection):
    """
    Finds the address string and updates the db with that information.
    """
    address_string = "{a} {s}, Jersey City, NJ".format(a=doc['Address'],
                                                       s=doc['Street'])

    add_geodata_to_doc(doc, collection, geocode.get_geocode_for_address(address_string))
    return True


def add_all_address_strings(collection):
    """
    Adds the address string to all documents in a collection.

    Will overwrite them if they already exist.
    """
    curs = collection.find()
    for doc in curs:
        add_geodata(doc, collection)
    return True


def main():
    opts = docopt(__doc__)
    hostname = opts['--host']
    port = int(opts['--port'])
    dbname = opts['--dbname']
#    collname = opts['--collname']
    collname = "sewMainWithGeo"
    client = pymongo.MongoClient(host=hostname, port=port)
    db = client[dbname]
    collection = db[collname]
    curs = collection.find(
        {
            "geodata.loc": {
                "$near" : {
                    "$geometry" : {
                        "type" : "Point",
                        "coordinates" : [-74.0944551, 40.7001318]
                    }
                }
            }
        }
    ).limit(100)

    str1 = ""
    str2 = ""
    index = 0
    for doc in curs:
        index += 1
        lat = doc["geodata"]["loc"]["coordinates"][1]
        long = doc["geodata"]["loc"]["coordinates"][0]
        name = doc["geodata"]["name"]
        str1 += """
            var myhouse{ind:d} = {{lat: {lat:f}, lng: {lng:f}}};
            var marker{ind:d} = new google.maps.Marker({{
                position: myhouse{ind:d}, map: map, title: 'First Marker!'
            }});
            var infowindow{ind:d} = new google.maps.InfoWindow({{
                content: "This is my infowindow {name}."
            }});
            """.format(ind=index, lat=lat, lng=long, name=name)

        str2 += """
            marker{index}.addListener('click', function() {{
                infowindow{index}.open(map, marker{index});
            }});
            """

    output = """
    <!DOCTYPE html>
    <html>
        <head>
          <style>
            html,
            body {{
                font-family: Arial, sans-serif;
                height: 100%;
                margin: 0;
                padding:0;
            }}

            #map {{
                height: 100%;
            }}
          </style>
        </head>
        <body>


    <div id="container2">
        abcacdf
        <!-- This element's contents will be replaced with your component. -->
    </div>
    abc
             <div id="map">def</div>


             <script>
                var map;
                function initMap() {{
                    console.log("In page");

                    // Constructor creates a new map - only center and zoom are required.
                    map = new google.maps.Map(document.getElementById('map'), {{
                        center : {{ lat : 40.704243, lng: -74.092521 }},
                        zoom: 15
                    }});

                    {str1part}


                    var locations = {{ title : 'home' , location : "myhouse" }};
                    {str2part}
                }}
             </script>
            <script async defer
              src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB_XksKhhz1Miqhw3Y8_LZcmAc90wypSiw&v=3&callback=initMap">
            </script>
        </body>
    </html>""".format(str1part=str1, str2part=str2)

    print("HELLO! " + output)


if __name__ == '__main__':
    main()
