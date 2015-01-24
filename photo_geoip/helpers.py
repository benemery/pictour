import exifread

class InvalidGPSData(Exception):
    pass

def extract_data(image):
    """Extract long / lat / time from image

    image is a file like object.
    """
    tags = exifread.process_file(image)

    lat = tags.get("EXIF GPS GPSLatitude", None)
    lng = tags.get("EXIF GPS GPSLongitude", None)

    lat_ref = tags.get("EXIF GPS GPSLatitudeRef", None)
    lng_ref = tags.get("EXIF GPS GPSLongitudeRef", None)

    if not lat or not lng or not lat_ref or not lng_ref:
        raise InvalidGPSData('Invalid GPS data: [lat: %s, lng: %s, lat_ref: %s, lng_ref: %s]' % (lat, lng, lat_ref, lng_ref))

    # We should use creation date from the image but f that for now.
    time = tags.get("EXIF GPS GPSDate", None)

    def r2f(ratio):
        return float(ratio.num) / ratio.den

    def ratio_to_value(component):
        component_floats = [r2f(ratio) for ratio in component.values]
        return component_floats[0] + component_floats[1] / 60 + component_floats[2] / 3600

    lat = ratio_to_value(lat)
    lng = ratio_to_value(lng)

    if lat_ref.values[0].lower() == "s":
        lat *= -1
    if lng_ref.values[0].lower() == "w":
        lng *= -1

    return lat, lng


from math import radians, cos, sin, asin, sqrt
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    Taken from: http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

def image_within_limit(lim_lat, lim_lon, image, error_margin=0.5):
    """Is this image within the boundary?"""
    lat, lon = extract_data(image)
    delta = haversine(lim_lat, lim_lon, lat, lon)
    return delta <= error_margin
