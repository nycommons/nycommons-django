import json
from urllib import urlencode

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag
from django import template


register = template.Library()


PLUTO_URL = 'http://www.nyc.gov/html/dcp/html/bytes/applbyte.shtml#pluto'


class GetZolaUrl(AsTag):
    options = Options(
        'for',
        Argument('lot', resolve=True, required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def get_value(self, context, lot):
        base = 'https://zola.planning.nyc.gov/l/lot/'
        if lot.bbl and not lot.bbl_is_fake:
            return '%s/%s/%s/%s' % (base, lot.bbl[0], lot.block, lot.lot_number)
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


register.tag(GetZolaUrl)
register.tag(GetOwnerMapUrl)
