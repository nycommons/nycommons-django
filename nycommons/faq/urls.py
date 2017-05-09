from django.conf.urls import url

from articles.views import ArticleList


urlpatterns = [
    url(r'^$', ArticleList.as_view(), name='faq_index'),
]
