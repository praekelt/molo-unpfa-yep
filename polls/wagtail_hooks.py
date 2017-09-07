from django.conf.urls import url
from polls.admin import QuestionsModelAdmin
from polls.admin_views import QuestionResultsAdminView
# from polls.models import PollsIndexPage
from wagtail.wagtailcore import hooks
from wagtail.contrib.modeladmin.options import modeladmin_register
from django.contrib.auth.models import User


@hooks.register('register_admin_urls')
def register_question_results_admin_view_url():
    return [
        url(r'polls/question/(?P<parent>\d+)/results/$',
            QuestionResultsAdminView.as_view(),
            name='question-results-admin'),
    ]


modeladmin_register(QuestionsModelAdmin)


@hooks.register('construct_main_menu')
def show_polls_entries_for_users_have_access(request, menu_items):
    if not request.user.is_superuser and not User.objects.filter(
            pk=request.user.pk, groups__name='Moderators').exists():
        menu_items[:] = [
            item for item in menu_items if item.name != 'polls']


# @hooks.register('construct_explorer_page_queryset')
# def hide_polls_index_page(parent_page, pages, request):
#     polls_index_page_pk = PollsIndexPage.objects.descendant_of(
#         request.site.root_page).first().pk
#     return pages.exclude(pk=polls_index_page_pk)
