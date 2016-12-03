from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import pymongo
import time


def index(request):
    collname = "sewMainWithGeo"
    hostname = "localhost"
    port = 27017
    client = pymongo.MongoClient()
    dbname = "jc"
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
            """.format(index=index)

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
    return HttpResponse(output)

