from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import BibEntry


class IndexView(ListView, LoginRequiredMixin):

    model = BibEntry
    paginate_by = 5


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
