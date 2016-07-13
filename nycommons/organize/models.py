from livinglots_organize.models import BaseOrganizer, BaseWatcher


class Organizer(BaseOrganizer):
    pass

class Watcher(BaseWatcher):
    pass


# Require email fields for both Organizer and Watcher instances
Organizer._meta.get_field('email').blank = False
Watcher._meta.get_field('email').blank = False
