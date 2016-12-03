import json
import urllib2
import urllib
import logging


# constants for the geocode API: https://developers.google.com/maps/documentation/geocoding/intro
geocode_apikey = "AIzaSyB_XksKhhz1Miqhw3Y8_LZcmAc90wypSiw"
geocode_urlbase = "https://maps.googleapis.com/maps/api/geocode/json?key=" + geocode_apikey

# logger
logger = logging.getLogger('main')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def get_geocode_for_address(street_address):
    geocode_params = { 'address' : street_address }
    geocode_url=geocode_urlbase + "&" + urllib.urlencode(geocode_params)
    logger.info("Fetcing via URL %s", geocode_url)
    data = json.load(urllib2.urlopen(geocode_url))
    location = data["results"][0]["geometry"]["location"]
    return {
        "location": {
            "type": "Point",
            "coordinates": [ location["lat"], location["lng"] ]
        },
        "name" : "abc"
    }


def main():
    location = get_geocode_for_address('201 Montgomery St, Jersey City, NJ')
    print("Location: lat={}, long={}".format(location.latitude, location.longitude))


if __name__ == '__main__':
    main()
