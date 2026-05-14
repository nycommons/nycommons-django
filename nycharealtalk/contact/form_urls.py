from django.conf.urls import url

from .views import ContactFormView

urlpatterns = [
    url('^$', ContactFormView.as_view(), name='form'),
]
