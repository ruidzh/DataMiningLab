import os
from django.contrib.gis.utils import LayerMapping
from .models import BoroughDistrict, CityDistrict

cty_mapping = { #state,
    'fip' : 'COUNTY_FIP',
    'name' : 'NAME',
    'shape' : 'MULTIPOLYGON',
}

cty_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data/CEN2000nycnty/cty036.shp'),
)

def cty_run(verbose=True):
    lm = LayerMapping(
        BoroughDistrict, cty_shp, cty_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)

    
nyc_mapping = {
    'area' : 'shape_area',
    'borough' : {'fip': 'county_fip'},
    'name' : 'ntaname',
    'shape' : 'MULTIPOLYGON',
    'ntacode' : 'ntacode'
}

nyc_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data/Neighborhood Tabulation Areas/Neighborhood Tabulation Areas.shp'),
)

def nyc_run(verbose=True):
    lm = LayerMapping(
        CityDistrict, nyc_shp, nyc_mapping,
        transform=False, encoding='iso-8859-1',
    )
    lm.save(strict=True, verbose=verbose)