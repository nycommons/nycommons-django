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


register.tag(GetOasisUrl)
