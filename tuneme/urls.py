import os

from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.contrib.wagtailsitemaps.views import sitemap
from django_cas_ng.views import login, logout, callback
from molo.profiles.views import RegistrationDone
from tuneme.views import report_response
from tuneme.forms import TunemeDoneForm
from molo.core.views import upload_file, download_file

from likes import urls as likes_urls
from molo.pwa import urls as pwa_urls
from molo.core import urls as core_urls
from molo.surveys import urls as surveys_urls
from molo.profiles import urls as profiles_urls
from molo.yourtips import urls as yourtips_urls
from molo.yourwords import urls as yourwords_urls
from molo.globalsite import urls as globalsite_urls
from molo.commenting import urls as commenting_urls
from molo.servicedirectory import urls as servicedirectory_urls
from django_comments import urls as django_comments_urls


# Path to a custom template that will be used by the admin
# site main index view.
admin.site.index_template = 'django_admin/index.html'
admin.autodiscover()

# implement CAS URLs in a production setting
if settings.ENABLE_SSO:
    urlpatterns = [
        url(r'^admin/login/', login),
        url(r'^admin/logout/', logout),
        url(r'^admin/callback/', callback),
    ]
else:
    urlpatterns = []

urlpatterns += [
    url(r'^django-admin/upload_media/',
        upload_file, name='molo_upload_media'),

    url(r'^django-admin/download_media/',
        download_file, name='molo_download_media'),

    url(r'^django-admin/', include(admin.site.urls)),
    url(r'', include(pwa_urls)),

    url(r'^admin/', include(wagtailadmin_urls)),

    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),

    url(r'^sitemap\.xml$', sitemap),

    url(r'', include(core_urls)),

    url(r'^globalsite/',
        include(
            globalsite_urls,
            namespace='molo.globalsite', app_name='molo.globalsite'
        )),

    url(r'^profiles/register/done/',
        login_required(RegistrationDone.as_view(
            template_name="profiles/done.html",
            form_class=TunemeDoneForm
        )),
        name='registration_done'),

    url(r'^profiles/', include(profiles_urls, namespace='molo.profiles')),

    url(r'^yourwords/', include(
        yourwords_urls, namespace='molo.yourwords'
    )),

    url(r'^yourtips/', include(
        yourtips_urls, namespace='molo.yourtips'
    )),

    url(r'^servicedirectory/', include(
        servicedirectory_urls,
        namespace='molo.servicedirectory'
    )),

    url(r'^likes/', include(
        likes_urls, namespace='likes', app_name='likes'
    )),

    url(r'^surveys/', include(
        surveys_urls, namespace='molo.surveys', app_name='molo.surveys'
    )),

    url(r'^comments/reported/(?P<comment_pk>\d+)/$',
        report_response, name='report_response'),

    url(r'^commenting/', include(
        commenting_urls,
        namespace='molo.commenting', app_name='molo.commenting'
    )),

    url(r'', include(django_comments_urls)),
    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(
                              settings.MEDIA_ROOT, 'images'))
