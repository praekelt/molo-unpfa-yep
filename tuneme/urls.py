import os

from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from molo.profiles.views import RegistrationDone
from tuneme.views import report_response
from tuneme.forms import TunemeDoneForm
from molo.core.views import upload_file, download_file


# Path to a custom template that will be used by the admin
# site main index view.
admin.site.index_template = 'django_admin/index.html'
admin.autodiscover()

# implement CAS URLs in a production setting
if settings.ENABLE_SSO:
    urlpatterns = patterns(
        '',
        url(r'^admin/login/', 'django_cas_ng.views.login'),
        url(r'^admin/logout/', 'django_cas_ng.views.logout'),
        url(r'^admin/callback/', 'django_cas_ng.views.callback'),
    )
else:
    urlpatterns = patterns('', )

urlpatterns += patterns(
    '',
    url(r'^django-admin/upload_media/', upload_file,
        name='molo_upload_media'),
    url(r'^django-admin/download_media/', download_file,
        name='molo_download_media'),
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml$', 'wagtail.contrib.wagtailsitemaps.views.sitemap'),

    url(r'', include('molo.core.urls')),

    url(r'^polls/', include('polls.urls',
                            namespace='polls')),
    url(
        r'^profiles/register/done/',
        login_required(RegistrationDone.as_view(
            template_name="profiles/done.html",
            form_class=TunemeDoneForm
        )),
        name='registration_done'
    ),
    url(r'^profiles/', include('molo.profiles.urls',
                               namespace='molo.profiles')),

    url(r'^yourwords/', include('molo.yourwords.urls',
                                namespace='molo.yourwords')),

    url(r'^servicedirectory/', include('molo.servicedirectory.urls',
        namespace='molo.servicedirectory')),

    url(r'^comments/reported/(?P<comment_pk>\d+)/$',
        report_response, name='report_response'),
    url(r'^commenting/', include('molo.commenting.urls',
        namespace='molo.commenting', app_name='molo.commenting')),
    url(r'', include('django_comments.urls')),
    url(r'', include(wagtail_urls)),
)


if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL + 'images/',
                          document_root=os.path.join(
                              settings.MEDIA_ROOT, 'images'))
