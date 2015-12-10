from django.contrib import admin
from django.core.urlresolvers import reverse

from polls.models import Question, Choice


class ParentListFilter(admin.SimpleListFilter):
    title = 'parent'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [(q.slug, q.title) for q in Question.objects.all()]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            parent = Question.objects.get(slug=self.value())
            return Choice.objects.child_of(parent).order_by('-id')
        return queryset


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('entries', 'live')
    fieldsets = (
        (
            None,
            {'fields': ('title', )}
        ),
    )
    readonly_fields = ['title']

    def entries(self, obj, *args, **kwargs):
        url = reverse('admin:polls_choice_changelist')
        return '<a href="%s?parent=%s">%s</a>' % (
            url, obj.slug, obj)

    entries.allow_tags = True
    entries.short_description = 'Title'


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'votes', 'live', '_parent')
    list_filter = (ParentListFilter, )
    fieldsets = (
        (
            None,
            {'fields': ('title', 'votes')}
        ),
    )
    readonly_fields = ['title', 'votes']

    def _parent(self, obj, *args, **kwargs):
        return obj.get_parent().title

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
