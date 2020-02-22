from django.contrib import admin

from .models import BibEntry, Author, Tag, Copy


class CopyInline(admin.StackedInline):
    model = Copy
    extra = 0


class BibEntryAdmin(admin.ModelAdmin):
    inlines = [CopyInline]

admin.site.register(BibEntry, BibEntryAdmin)
admin.site.register([Author, Tag])