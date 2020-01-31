from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import BibEntry

@login_required
def index(request):
    entries = BibEntry.objects.all()
    q = request.GET.get('q')
    if q:
        entries = BibEntry.objects.filter(title__icontains=q)

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

    context = {
        'entries': data
    }
    return render(request, 'biblio/index.html', context)

@login_required
def detail(request, entry_id):
    entry = BibEntry.objects.get(pk=entry_id)
    data = {
        'id':entry_id,
        'title': entry.title,
        'authors': entry.authors.all(),
        'copies': entry.copy_set.all()
    }
    
    return render(request, 'biblio/detail.html', {'data':data})
