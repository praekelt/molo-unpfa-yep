from __future__ import unicode_literals

import json
from django.conf import settings
from django.http import QueryDict
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.utils import cautious_slugify

from molo.core.models import ArticlePage
from molo.commenting.models import MoloComment
from molo.surveys.models import SurveysIndexPage
from molo.servicedirectory.views import (
    OrganisationResultsView,
    make_request_to_google_api,
    get_google_places_api_server_key,
    get_service_directory_api_base_url,
    make_request_to_servicedirectory_api,
)


def report_response(request, comment_pk):
    comment = MoloComment.objects.get(pk=comment_pk)

    return render(request, 'comments/report_response.html', {
        'article': comment.content_object,
    })


def submission_article(request, survey_id, submission_id):
    # get the specific submission entry
    survey_page = get_object_or_404(Page, id=survey_id).specific
    SubmissionClass = survey_page.get_submission_class()

    submission = SubmissionClass.objects.filter(
        page=survey_page).filter(pk=submission_id).first()
    if not submission.article_page:
        survey_index_page = (
            SurveysIndexPage.objects.descendant_of(
                request.site.root_page).live().first())

        body = []
        for key, value in submission.get_data().items():
            if key not in [u'username', u'created_at']:
                body.append({"type": "paragraph", "value": str(value)})

        article = ArticlePage(
            title='yourwords-entry-%s' % cautious_slugify(submission_id),
            slug='yourwords-entry-%s' % cautious_slugify(submission_id),
            body=json.dumps(body)
        )
        survey_index_page.add_child(instance=article)
        article.save_revision()
        article.unpublish()

        submission.article_page = article
        submission.save()
        return redirect('/admin/pages/%d/move/' % article.id)
    return redirect('/admin/pages/%d/edit/' % submission.article_page.id)


class TMOrganisationResultsView(OrganisationResultsView):

    def get_context_data(self, **kwargs):
        context = super(OrganisationResultsView, self).get_context_data(
            **kwargs
        )

        place_id = self.request.GET.get('place_id')
        search_term = self.request.GET.get('search')
        location_term = self.request.GET.get('location')
        place_latlng = self.request.GET.get('place_latlng')
        place_formatted_address = self.request.GET.get(
            'place_formatted_address')

        radius = self.request.GET.get(
            'radius', settings.SERVICE_DIRECTORY_RESULT_LOCATION_RADIUS)

        if place_latlng is None:
            google_query_parms = QueryDict('', mutable=True)
            google_query_parms['placeid'] = place_id
            google_query_parms['key'] = get_google_places_api_server_key(
                self.request)

            url = 'https://maps.googleapis.com/maps/api/place/details/json'
            place_details = make_request_to_google_api(url, google_query_parms)

            place_details_result = place_details.get('result', {})

            place_formatted_address = place_details_result.get(
                'formatted_address', None
            )
            place_location = place_details_result.get(
                'geometry', {}
            ).get('location', None)

            if place_location:
                place_latlng = '{0},{1}'.format(
                    place_location['lat'], place_location['lng']
                )

        service_directory_query_parms = QueryDict('', mutable=True)
        # set the radius in which we would like to restrict the result set by
        service_directory_query_parms['radius'] = radius
        service_directory_query_parms['search_term'] = search_term

        if place_latlng is not None:
            service_directory_query_parms['location'] = place_latlng

        if place_formatted_address is not None:
            service_directory_query_parms['place_name'] =\
                place_formatted_address

        url = '{0}search/?{1}'.format(
            get_service_directory_api_base_url(self.request),
            service_directory_query_parms.urlencode()
        )
        search_results = make_request_to_servicedirectory_api(
            url, self.request)

        categories_keywords = []
        if not search_results:
            # TODO: consider caching the categories and keywords when we fetch
            # them for the home page, then retrieving them from the cache here
            categories_keywords_url = '{0}homepage_categories_keywords/'\
                .format(get_service_directory_api_base_url(self.request))

            categories_keywords = make_request_to_servicedirectory_api(
                categories_keywords_url,
                self.request
            )

        location_query_parms = QueryDict('', mutable=True)
        location_query_parms['location'] = location_term
        location_query_parms['search'] = search_term

        context['radius'] = radius
        context['place_id'] = place_id
        context['search_term'] = search_term
        context['place_latlng'] = place_latlng
        context['location_term'] = location_term
        context['place_formatted_address'] = place_formatted_address
        context['change_location_url'] = '{0}?{1}'.format(
            reverse('molo.servicedirectory:location-results'),
            location_query_parms.urlencode()
        )
        context['search_results'] = search_results
        context['categories_keywords'] = categories_keywords

        return context
