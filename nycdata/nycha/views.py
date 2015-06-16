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
        try:
            # XXX This appears to be a django-cachalot bug--all the counts came
            # back as 0 before invalidating
            from cachalot.api import invalidate_models
            invalidate_models([Lot,])
        except ImportError:
            pass
        return {
            'id': place.pk,
            'name': place.name,
            'lots_within': Lot.visible.filter(centroid__within=place.geom).count(),
            'projects_within': Lot.visible.filter(
                known_use__visible=True,
                centroid__within=place.geom
            ).count(),
        }
