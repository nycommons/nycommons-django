from django.dispatch import Signal


# Indicates that a Lot's details page is being loaded
lot_details_loaded = Signal(providing_args=['instance',])
