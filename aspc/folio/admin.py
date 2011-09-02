from django.contrib import admin
from aspc.folio.models import Page

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "short_title", "slug", "parent")

admin.site.register(Page, PageAdmin)