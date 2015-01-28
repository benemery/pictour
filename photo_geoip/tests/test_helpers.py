import os


from photo_geoip.helpers import extract_data, image_within_limit

CURRENT_DIR = os.path.dirname(__file__)

class TestGeoDataExtraction():
    def test_lon_lat(self):
        """Can we extract location data"""
        path = os.path.join(CURRENT_DIR, "test_image_1.jpg")
        with open(path, 'rb') as fin:
            lat, lon = extract_data(fin)
            assert lat == 51.524575
            assert lon == -0.07884722222222222

class TestImageLimit():
    def test_within_boundary(self):
        """Can we compare to lon / lats?"""
        path = os.path.join(CURRENT_DIR, "test_image_1.jpg")
        with open(path, 'rb') as fin:
            lat2 = 51.52534
            lon2 = -0.07754
            assert image_within_limit(lat2, lon2, fin)
