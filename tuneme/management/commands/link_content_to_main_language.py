from django.core.management.base import BaseCommand
from molo.core.models import LanguageRelation, Main, Languages
from wagtail.wagtailcore.models import Page


class Command(BaseCommand):
    def handle(self, *args, **options):
        for main in Main.objects.all():
            main_lang = Languages.for_site(main.get_site()).languages.filter(
                is_active=True, is_main_language=True).first()
            if main_lang:
                for page in Page.objects.descendant_of(main):
                    relation, created = LanguageRelation.objects.get_or_create(
                        page=page, language=main_lang
                    )
                    page = Page.objects.get(pk=relation.page.pk).specific
                    page.language = relation.language
                    page.save()
