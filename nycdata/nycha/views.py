import geojson
import json

from inplace.views import GeoJSONListView

from lots.models import Lot

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
            'lots_within': Lot.objects.filter(centroid__within=place.geom).count(),
            'projects_within': Lot.objects.filter(
                known_use__visible=True,
                centroid__within=place.geom
            ).count(),
        }
