from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core import serializers

from .models import BibEntry


def index(request):
    entries = BibEntry.objects.all()
    data = serializers.serialize("json", BibEntry.objects.all())

    data = [
        {
            'id': entry.id,
            'title': entry.title,
            'authors': ', '.join(str(a) for a in entry.authors.all()),
            'year': entry.year,
            'tags': ', '.join(str(a) for a in entry.tags.all())
        }
        for entry in entries
    ]

    print(data)

    context = {
        'entry_list': entries,
        'data': data
    }
    return render(request, 'biblio/index.html', context)

def detail(request, entry_id):
    entry = BibEntry.objects.get(pk=entry_id)
    data = {
        'id':entry_id,
        'title': entry.title,
        'authors': entry.authors.all(),
        'copies': entry.copy_set.all()
    }
    
    return render(request, 'biblio/detail.html', {'data':data})
