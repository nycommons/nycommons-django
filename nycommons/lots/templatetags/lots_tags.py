import json
from urllib import urlencode

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template


register = template.Library()


PLUTO_URL = 'http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml#pluto'


class GetOasisUrl(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        base = 'http://oasisnyc.net/map.aspx?etabs=1&zoomto='
        if lot.bbl and not lot.bbl_is_fake:
            return '%slot:%s' % (base, lot.bbl)
        try:
            return '%sgarden:%s' % (
                base,
                lot.steward_projects.all()[0].external_id,
            )
        except Exception:
            pass
        return None


class GetOwnerMapUrl(AsTag):
    """
    Get a map url that will filter the data on the map to just the owner and
    commons type that this lot is.
    """
    options = Options(
        Argument('organizing', default=False, resolve=True, required=False),
        Argument('priority', default=False,  resolve=True, required=False),
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, organizing, priority, lot):
        owners = {}
        owners[lot.commons_type] = [lot.owner.pk,]
        params = {
            'layers': json.dumps([lot.commons_type,]),
            'owners': json.dumps(owners),
        }
        if organizing:
            params['organizing'] = 'true'
        if priority:
            params['priority'] = 'true'
        return '/#%s' % urlencode(params)


register.tag(GetOasisUrl)
register.tag(GetOwnerMapUrl)
