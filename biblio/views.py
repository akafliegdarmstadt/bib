from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.contrib.auth.decorators import login_required

from .models import BibEntry


class IndexView(LoginRequiredMixin, ListView):

    model = BibEntry
    paginate_by = 5

    def get_queryset(self):
        search_val = self.request.GET.get('search')
        if search_val:
            new_context = BibEntry.objects.filter(
                title__icontains=search_val
            )
        else:
            new_context = BibEntry.objects.all()

        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        return context

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
