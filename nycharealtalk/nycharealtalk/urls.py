from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from registration.forms import AuthenticationForm

admin.autodiscover()

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
                     show_indexes=True)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += (
    # Living Lots
    url(r'^lots/(?P<pk>\d+)/content/',
        include('usercontent.urls', 'usercontent')),
    url(r'^lots/(?P<pk>\d+)/groundtruth/',
        include('groundtruth.urls', 'groundtruth')),
    url(r'^lots/(?P<pk>\d+)/organize/steward/',
        include('steward.urls', 'steward')),
    url(r'^lots/(?P<pk>\d+)/organize/',
        include('organize.urls', 'organize')),
    url(r'^lots/', include('lots.urls', 'lots')),
    url(r'^owners/', include('owners.urls', 'owners')),

    # Activity stream
    url('^activity/', include('activities.urls')),

    # Inplace
    url(r'^inplace/', include('inplace.urls', 'inplace')),

    # Django.js
    url(r'^djangojs/', include('djangojs.urls')),

    # Admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    # Auth
    url(r'^login/', auth_views.login, {
        'authentication_form': AuthenticationForm,
    }),

    # FeinCMS
    url(r'', include('feincms.urls')),

    url(r'^updates/', include('elephantblog.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

from django.shortcuts import render

from feincms.module.page.models import Page


def page_not_found(request, template_name='404.html'):
    page = Page.objects.best_match_for_path(request.path)
    return render(request, template_name, {'feincms_page': page}, status=404)


def error_handler(request, template_name='500.html'):
    page = Page.objects.best_match_for_path(request.path)
    return render(request, template_name, {'feincms_page': page}, status=500)


handler404 = page_not_found
handler500 = error_handler
