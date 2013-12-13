from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, RedirectView
from reviewz import settings

admin.autodiscover()


class ReveiwzIndex(TemplateView):
    template_name = 'reviewz_home.html'


urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url='/reviews/')),
    url(r'^reviews/',  include('reviewz.apps.peerreview.urls')),
    url(r'^accounts/', include('reviewz.apps.accounts.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
