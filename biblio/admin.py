from django.contrib import admin

from .models import BibEntry, Author, Tag, Copy

admin.site.register([BibEntry, Author, Tag, Copy])