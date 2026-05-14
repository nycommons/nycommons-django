from django.conf.urls import url

from .views import ContactFormView, ContactCompleted

form_urls = [
    url('^$', ContactFormView.as_view(), name='form'),
]


success_urls = [
    url('^success/$', ContactCompleted.as_view(), name='completed'),
]

urlpatterns = form_urls + success_urls
