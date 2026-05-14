from django.conf.urls import url

from .views import LotsMap


urlpatterns = [
    url(r'^', LotsMap.as_view()),
]
