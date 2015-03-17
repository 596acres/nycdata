from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet

from ..bbls import build_bbl


# This is an auto-generated Django model module created by ogrinspect using the
# following invocation:
#
#  django-admin ogrinspect $PLUTO_DIR/14v1/Staten_Island/test.shp Parcel 
#   --mapping --multi-geom --srid 4326
#
# The only modification is that the bbl field was changed to DecimalField since
# bbls are too large for IntegerField.

boroughs = {
    'BX': 'Bronx',
    'BK': 'Brooklyn',
    'MN': 'Manhattan',
    'QN': 'Queens',
    'SI': 'Staten Island',
}


class ParcelQuerySet(GeoQuerySet):

    def with_bbl(self, bbl=None, borough=None, block=None, lot=None):
        """Filter by bbl, creating one first if not provided."""
        if not bbl:
            bbl = build_bbl(borough, block, lot)
        return self.filter(bbl=bbl)


class ParcelManager(models.GeoManager):

    def get_queryset(self):
        return ParcelQuerySet(self.model, using=self._db)

    def with_bbl(self, **kwargs):
        return self.get_queryset().with_bbl(**kwargs)


class Parcel(models.Model):
    borough = models.CharField(max_length=2)
    block = models.IntegerField()
    lot_number = models.IntegerField()
    cd = models.IntegerField()
    ct2010 = models.CharField(max_length=7)
    cb2010 = models.CharField(max_length=5)
    schooldist = models.CharField(max_length=2)
    council = models.IntegerField()
    zipcode = models.IntegerField()
    firecomp = models.CharField(max_length=4)
    policeprct = models.IntegerField()
    address = models.CharField(max_length=28)
    zonedist1 = models.CharField(max_length=9)
    zonedist2 = models.CharField(max_length=9)
    zonedist3 = models.CharField(max_length=9)
    zonedist4 = models.CharField(max_length=9)
    overlay1 = models.CharField(max_length=4)
    overlay2 = models.CharField(max_length=4)
    spdist1 = models.CharField(max_length=6)
    spdist2 = models.CharField(max_length=6)
    ltdheight = models.CharField(max_length=5)
    allzoning1 = models.CharField(max_length=27)
    allzoning2 = models.CharField(max_length=21)
    splitzone = models.CharField(max_length=1)
    bldgclass = models.CharField(max_length=2)
    landuse = models.CharField(max_length=2)
    easements = models.IntegerField()
    ownertype = models.CharField(max_length=1)
    ownername = models.CharField(max_length=21)
    lotarea = models.IntegerField()
    bldgarea = models.IntegerField()
    comarea = models.IntegerField()
    resarea = models.IntegerField()
    officearea = models.IntegerField()
    retailarea = models.IntegerField()
    garagearea = models.IntegerField()
    strgearea = models.IntegerField()
    factryarea = models.IntegerField()
    otherarea = models.IntegerField()
    areasource = models.CharField(max_length=1)
    numbldgs = models.IntegerField()
    numfloors = models.FloatField()
    unitsres = models.IntegerField()
    unitstotal = models.IntegerField()
    lotfront = models.FloatField()
    lotdepth = models.FloatField()
    bldgfront = models.FloatField()
    bldgdepth = models.FloatField()
    ext = models.CharField(max_length=2)
    proxcode = models.CharField(max_length=1)
    irrlotcode = models.CharField(max_length=1)
    lottype = models.CharField(max_length=1)
    bsmtcode = models.CharField(max_length=1)
    assessland = models.FloatField()
    assesstot = models.FloatField()
    exemptland = models.FloatField()
    exempttot = models.FloatField()
    yearbuilt = models.IntegerField()
    builtcode = models.CharField(max_length=1)
    yearalter1 = models.IntegerField()
    yearalter2 = models.IntegerField()
    histdist = models.CharField(max_length=40)
    landmark = models.CharField(max_length=35)
    builtfar = models.FloatField()
    residfar = models.FloatField()
    commfar = models.FloatField()
    facilfar = models.FloatField()
    borocode = models.IntegerField()
    bbl = models.DecimalField(max_digits=10, decimal_places=0, db_index=True)
    condono = models.IntegerField()
    tract2010 = models.CharField(max_length=6)
    xcoord = models.IntegerField()
    ycoord = models.IntegerField()
    zonemap = models.CharField(max_length=3)
    zmcode = models.CharField(max_length=1)
    sanborn = models.CharField(max_length=8)
    taxmap = models.CharField(max_length=5)
    edesignum = models.CharField(max_length=5)
    appbbl = models.FloatField()
    appdate = models.CharField(max_length=10)
    plutomapid = models.CharField(max_length=1)
    version = models.CharField(max_length=4)
    mappluto_f = models.IntegerField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    objects = ParcelManager()

    def __unicode__(self):
        return str(self.bbl)

    def _borough_name(self):
        return boroughs[self.borough]
    borough_name = property(_borough_name)

    def bldgclass_vacant(self):
        """Does this parcel have a vacant building class?"""
        return self.bldgclass.lower().startswith('v')

    def landuse_vacant(self):
        """Does this parcel have a vacant landuse?"""
        return self.landuse == '11'


# Auto-generated `LayerMapping` dictionary for Parcel model
parcel_mapping = {
    'borough' : 'Borough',
    'block' : 'Block',
    'lot_number' : 'Lot',
    'cd' : 'CD',
    'ct2010' : 'CT2010',
    'cb2010' : 'CB2010',
    'schooldist' : 'SchoolDist',
    'council' : 'Council',
    'zipcode' : 'ZipCode',
    'firecomp' : 'FireComp',
    'policeprct' : 'PolicePrct',
    'address' : 'Address',
    'zonedist1' : 'ZoneDist1',
    'zonedist2' : 'ZoneDist2',
    'zonedist3' : 'ZoneDist3',
    'zonedist4' : 'ZoneDist4',
    'overlay1' : 'Overlay1',
    'overlay2' : 'Overlay2',
    'spdist1' : 'SPDist1',
    'spdist2' : 'SPDist2',
    'ltdheight' : 'LtdHeight',
    'allzoning1' : 'AllZoning1',
    'allzoning2' : 'AllZoning2',
    'splitzone' : 'SplitZone',
    'bldgclass' : 'BldgClass',
    'landuse' : 'LandUse',
    'easements' : 'Easements',
    'ownertype' : 'OwnerType',
    'ownername' : 'OwnerName',
    'lotarea' : 'LotArea',
    'bldgarea' : 'BldgArea',
    'comarea' : 'ComArea',
    'resarea' : 'ResArea',
    'officearea' : 'OfficeArea',
    'retailarea' : 'RetailArea',
    'garagearea' : 'GarageArea',
    'strgearea' : 'StrgeArea',
    'factryarea' : 'FactryArea',
    'otherarea' : 'OtherArea',
    'areasource' : 'AreaSource',
    'numbldgs' : 'NumBldgs',
    'numfloors' : 'NumFloors',
    'unitsres' : 'UnitsRes',
    'unitstotal' : 'UnitsTotal',
    'lotfront' : 'LotFront',
    'lotdepth' : 'LotDepth',
    'bldgfront' : 'BldgFront',
    'bldgdepth' : 'BldgDepth',
    'ext' : 'Ext',
    'proxcode' : 'ProxCode',
    'irrlotcode' : 'IrrLotCode',
    'lottype' : 'LotType',
    'bsmtcode' : 'BsmtCode',
    'assessland' : 'AssessLand',
    'assesstot' : 'AssessTot',
    'exemptland' : 'ExemptLand',
    'exempttot' : 'ExemptTot',
    'yearbuilt' : 'YearBuilt',
    'builtcode' : 'BuiltCode',
    'yearalter1' : 'YearAlter1',
    'yearalter2' : 'YearAlter2',
    'histdist' : 'HistDist',
    'landmark' : 'Landmark',
    'builtfar' : 'BuiltFAR',
    'residfar' : 'ResidFAR',
    'commfar' : 'CommFAR',
    'facilfar' : 'FacilFAR',
    'borocode' : 'BoroCode',
    'bbl' : 'BBL',
    'condono' : 'CondoNo',
    'tract2010' : 'Tract2010',
    'xcoord' : 'XCoord',
    'ycoord' : 'YCoord',
    'zonemap' : 'ZoneMap',
    'zmcode' : 'ZMCode',
    'sanborn' : 'Sanborn',
    'taxmap' : 'TaxMap',
    'edesignum' : 'EDesigNum',
    'appbbl' : 'APPBBL',
    'appdate' : 'APPDate',
    'plutomapid' : 'PLUTOMapID',
    'version' : 'Version',
    'mappluto_f' : 'MAPPLUTO_F',
    'shape_leng' : 'SHAPE_Leng',
    'shape_area' : 'SHAPE_Area',
    'geom' : 'MULTIPOLYGON',
}
