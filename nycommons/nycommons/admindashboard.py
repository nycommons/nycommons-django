from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard import modules, Dashboard


class LivingLotsDashboard(Dashboard):
    columns = 3

    def __init__(self, **kwargs):

        self.children = self.children or []

        self.children.append(modules.ModelList(
            title=_('Site Content'),
            models=(
                'blog.*',
                'faq.*',
                'feincms.module.page.*',
                'organizingpathways.*',
                'ownerpathways.*',
                'reviewpathways.*',
            ),
        ))

        self.children.append(modules.AppList(
            title=_('Applications'),
            exclude=(
                'actstream.*',
                'articles.*',
                'blog.*',
                'django.contrib.*',
                'elephantblog.*',
                'faq.*',
                'feincms.module.medialibrary.*',
                'feincms.module.page.*',
                'flatblocks.*',
                'inplace.boundaries.*',
                'livinglots_lots.*',
                'livinglots_mailings.*',
                'livinglots_organize.*',
                'livinglots_owners.*',
                'livinglots_usercontent.*',
                'lots.*',
                'nycdata.citycouncildistricts.*',
                'nycdata.communitydistricts.*',
                'organize.*',
                'organizingpathways.*',
                'ownerpathways.*',
                'owners.*',
                'reviewpathways.*',
                'taggit.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Lot Content'),
            models=('livinglots_usercontent.*',),
        ))

        self.children.append(modules.ModelList(
            title=_('Lots'),
            models=(
                'livinglots_lots.*',
                'lots.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Owners'),
            models=(
                'livinglots_owners.*',
                'owners.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Participants'),
            models=(
                'livinglots_organize.*',
                'organize.*',
            ),
        ))

        self.children.append(modules.ModelList(
            title=_('Political Representation'),
            models=(
                'nycdata.citycouncildistricts.*',
                'nycdata.communitydistricts.*',
            ),
        ))

        self.children.append(modules.AppList(
            title=_('Administration'),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.AppList(
            title=_('Advanced'),
            models=(
                'actstream.*',
                'feincms.module.medialibrary.*',
                'flatblocks.*',
                'inplace.boundaries.*',
                'livinglots_mailings.*',
                'taggit.*',
            ),
        ))

        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            limit=5
        ))
