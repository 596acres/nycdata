import geojson
import json

from inplace.views import GeoJSONListView

from .models import NYCHADevelopment


class NYCHAGeoJSONListView(GeoJSONListView):
    model = NYCHADevelopment

    def get_feature(self, place):
        return geojson.Feature(
            place.pk,
            geometry=json.loads(place.geom.geojson),
            properties=self.get_properties(place),
        )

    def get_properties(self, place):
        return {
            'id': place.pk,
            'name': place.name,
        }
