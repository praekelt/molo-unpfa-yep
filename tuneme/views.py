from __future__ import unicode_literals

import json
from django.shortcuts import render, get_object_or_404, redirect

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.utils import cautious_slugify

from molo.core.models import ArticlePage
from molo.commenting.models import MoloComment
from molo.surveys.models import SurveysIndexPage


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
            if key != 'username':
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
