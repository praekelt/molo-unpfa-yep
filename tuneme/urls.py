import os

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from molo.profiles.views import RegistrationDone
from tuneme.views import search, report_message
from tuneme.forms import DateOfBirthForm


urlpatterns = patterns(
    '',
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'', include('molo.core.urls')),

    url(r'^polls/', include('polls.urls',
                            namespace='molo.polls')),
    url(
        r'^profiles/register/done/',
        login_required(RegistrationDone.as_view(
            template_name="profiles/done.html",
            form_class=DateOfBirthForm
        )),
        name='registration_done'
    ),
    url(r'^profiles/', include('molo.profiles.urls',
                               namespace='molo.profiles')),
    url(r'^comments/reported/(\d+)', report_message, name='report-message'),
    url(r'^comments/', include('molo.commenting.urls')),
    url(r'search/$', search, name='search'),
    url(r'', include(wagtail_urls)),

    url(r'^djga/', include('google_analytics.urls')),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(
                              settings.MEDIA_ROOT, 'images'))
