from django.conf.urls import url

from .models import GroundtruthRecord
from .views import AddGroundtruthRecordView


urlpatterns = (

    url(r'^add/$', AddGroundtruthRecordView.as_view(),
        name='add_groundtruthrecord'),

)
