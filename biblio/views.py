from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.views import generic
from django.views.generic.list import ListView
from django.db.models import Q

from .models import BibEntry


class IndexView(LoginRequiredMixin, ListView):

    model = BibEntry
    paginate_by = 20

    def get_queryset(self):        
        query_parts = []

        search_val = self.request.GET.get('search')
        if search_val:
            query_parts.append(
                Q(title__icontains=search_val) | Q(authors__name__icontains=search_val)
            )
        
        tags_val = self.request.GET.get('tags')
        if tags_val:
            query_parts.append(Q(tags__name__in=tags_val.split(',')))

        queryset = BibEntry.objects.filter(*query_parts).distinct()

        sort_val = self.request.GET.get('sort')

        if sort_val and sort_val.replace('-','') in ('title', 'year'):
            return queryset.order_by(sort_val)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        context['sort'] = self.request.GET.get('sort')
        context['tags'] = self.request.GET.get('tags')
        context['taglist'] = self.request.GET.get('tags').split(',')
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
