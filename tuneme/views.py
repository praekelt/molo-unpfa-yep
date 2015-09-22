from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from molo.core.models import ArticlePage
from molo.core.models import LanguagePage
from molo.core.utils import get_locale_code
from molo.commenting.models import MoloComment
from wagtail.wagtailsearch.models import Query


def search(request, results_per_page=10):
    search_query = request.GET.get('q', None)
    page = request.GET.get('p', 1)

    if search_query:
        results = ArticlePage.objects.live().search(search_query)
        Query.get(search_query).add_hit()
    else:
        results = ArticlePage.objects.none()

    paginator = Paginator(results, results_per_page)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(request, 'search/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
        'results': results,
    })

def report_response(request, comment_pk):
    comment = MoloComment.objects.get(pk=comment_pk)
    language_page = LanguagePage.objects.get(code=get_locale_code())

    return render(request, 'comments/report_response.html', {
        'article': comment.content_object,
        'language_page': language_page
    })
