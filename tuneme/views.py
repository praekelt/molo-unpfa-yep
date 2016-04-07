import django_comments
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from molo.commenting import MoloCommentForm

from molo.core.models import ArticlePage
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

    return render(request, 'comments/report_response.html', {
        'article': comment.content_object,
    })


class CommentReplyFormView(TemplateView):
    form_class = MoloCommentForm
    template_name = 'comments/reply.html'

    def get(self, request, parent_id):
        comment = get_object_or_404(
            django_comments.get_model(), pk=parent_id,
            site__pk=settings.SITE_ID)
        form = MoloCommentForm(comment.content_object, initial={
            'content_type': '%s.%s' % (
                comment.content_type.app_label,
                comment.content_type.model),
            'object_pk': comment.object_pk,
        })
        return self.render_to_response({
            'form': form,
            'comment': comment,
        })