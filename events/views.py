from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views import generic, View
from django.core.mail import send_mail
from django.db.models import Count
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django import forms
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.http import HttpResponseRedirect

from .models import Event, EventComment
from .forms import CommentForm, EventForm, DocumentFormSet, ObservablesFormSet, ThreatActorsFormSet
from . import models
from users.models import User
from users.views import UserCanViewDataMixin


from django.conf import settings
from django.http import HttpResponse
import os
from dal import autocomplete
from common.models import Sector, Motive
from django_countries import countries

from rest_framework import viewsets

from . import serializers

import json
from django import http

def download(request, path):
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/text")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    raise Http404

class SectorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Sector.objects.none()

        qs = Sector.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class MotiveAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Motive.objects.none()

        qs = Motive.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


from dal.views import ViewMixin

class Select2ViewMixin(object):
    """View mixin to render a JSON response for Select2."""

    def get_results(self, context):
        """Return data for the 'results' key of the response."""
        return [
            {
                'id': self.get_result_value(result),
                'text': self.get_result_label(result),
                'selected_text': self.get_selected_result_label(result),
            } for result in context['object_list']
        ]

    def get_create_option(self, context, q):
        """Form the correct create_option to append to results."""
        create_option = []
        display_create_option = False
        if self.create_field and q:
            page_obj = context.get('page_obj', None)
            if page_obj is None or page_obj.number == 1:
                display_create_option = True

            # Don't offer to create a new option if a
            # case-insensitive) identical one already exists
            existing_options = (self.get_result_label(result).lower()
                                for result in context['object_list'])
            if q.lower() in existing_options:
                display_create_option = False

        if display_create_option and self.has_add_permission(self.request):
            create_option = [{
                'id': q,
                'text': _('Create "%(new_value)s"') % {'new_value': q},
                'create_id': True,
            }]
        return create_option

    def render_to_response(self, context):
        """Return a JSON response in Select2 format."""
        q = self.request.GET.get('q', None)

        create_option = self.get_create_option(context, q)

        return http.HttpResponse(
            json.dumps({
                'results': self.get_results(context) + create_option,
                'pagination': {
                    'more': self.has_more(context)
                }
            }),
            content_type='application/json',
        )


#class CountryAutocompleteFromList(ViewMixin, View):
#    """Autocomplete from a list of items rather than a QuerySet."""
#
##    def get_list(self):
##        """Return the list strings from which to autocomplete."""
###        return []
##
##        return [
##            {
##                'id': self.get_result_value(result),
##                'text': self.get_result_label(result),
##                'selected_text': self.get_selected_result_label(result),
##            } for result in context['object_list']
##        ]
#
#    def get_list(self):
#        contries_dict = countries.countries
#        country_dict = dict()
#        for index, key in enumerate(contries_dict.keys()):
#            country_dict['id'] = index
#            country_dict['text'] = str(contries_dict[key])
#            country_dict['selected_text'] = str(key)
#            #print(country_dict)
#
##        return ['Estionia', 'Finland']
#        return country_dict
#
#    def get(self, request, *args, **kwargs):
#        """Return option list json response."""
#        results = self.get_list()
#        create_option = []
#        if self.q:
#            print(self.q)
#            results = self.results(results)
#            print(results)
#            if hasattr(self, 'create'):
#                create_option = [{
#                    'id': self.q,
#                    'text': 'Create "%s"' % self.q,
#                    'create_id': True
#                }]
#
#        print(self.results(results))
#        return http.HttpResponse(json.dumps({
#            'results': self.results(results),
#            'pagination': {'more': False} 
#        }), content_type='application/json')
#
#    def autocomplete_results(self, results):
#        """Return list of strings that match the autocomplete query."""
#        return [x for x in results if self.q.lower() in x.lower()]
#
#    def results(self, results):
#        """Return the result dictionary."""
#        #return [dict(id=x, text=x) for x in results]
#        print(results)
#        return results
#
#    def post(self, request):
#        """Add an option to the autocomplete list.
#        If 'text' is not defined in POST or self.create(text) fails, raises
#        bad request. Raises ImproperlyConfigured if self.create if not defined.
#        """
#        if not hasattr(self, 'create'):
#            raise ImproperlyConfigured('Missing "create()"')
#
#        text = request.POST.get('text', None)
#
#        if text is None:
#            return http.HttpResponseBadRequest()
#
#        text = self.create(text)
#
#        if text is None:
#            return http.HttpResponseBadRequest()
#
#        return http.HttpResponse(json.dumps({
#            'id': text,
#            'text': text,
#        }))

from dal.autocomplete import Select2ListView

class CountryAutocompleteFromList(Select2ListView):


    def get_list(self):
        contries_dict = countries.countries
        countries_list = list()
        for key, value in contries_dict.items():
            countries_list.append(str(value))

        return contries_dict

    def autocomplete_results(self, results):
        """Return list of strings that match the autocomplete query."""
        if self.q in results.values():
            print(self.q)

        #return dict()

        return [dict(id=str(key), text=str(value)) for key, value in results.items() if self.q.lower() in value.lower()]
#        print(results[self.q])
#        return (results[self.q])
#        return [x for x in results.values() if self.q.lower() in x.lower()]


    def results(self, results):
        """Return the result dictionary."""

        if isinstance(results, dict):
            return [dict(id=str(key), text=str(value)) for key, value in results.items()]

        else:
            return [x for x in results]


    def get(self, request, *args, **kwargs):
        """Return option list json response."""
        results = self.get_list()
        create_option = []
        if self.q:
            results = self.autocomplete_results(results)

        return http.HttpResponse(json.dumps({
            'results': self.results(results),
            'pagination': {'more': False} 
        }), content_type='application/json')



import django_tables2 as tables
import itertools
from django_tables2.utils import A
from django.utils.html import format_html

class TagData(tables.Table):
    class Meta:
        model = Tag


class EventTable(tables.Table):

    title = tables.LinkColumn(viewname=None)
    tag = tables.Column(empty_values=(), orderable=False)
    actions = tables.Column(empty_values=(), orderable=False)

    def __init__(self, *args, **kwargs):
        super(EventTable, self).__init__(*args, **kwargs)
        self.events = self.data.data
        self.tags_list = list()
        self.counter = itertools.count()
        self.index = 0
        self.events_list = list()
        for event in self.events:
            self.events_list.append(event)

    def render_tag(self):
        self.index = next(self.counter)
        tag_names = list()
        # this may bite me in the nether regions at some point, uhh ugly
        index = self.index
        for tag in self.events_list[index].tag.all():
            url = (reverse('events:event_list') + "?tag=%s" % tag.id)
            html = format_html(' <a href="%s">%s</a> '% (url, tag.name))
            tag_names.append(html)
        return format_html(' '.join(tag_names))

    def render_actions(self):
        index = self.index
        row = self.data.data[index]
        edit = format_html(' <a href="%s">%s</a> ' % (row.get_absolute_url() + "/edit", "edit"))
        delete = format_html(' <a href="%s">%s</a> ' % (row.get_absolute_url() + "/delete", "delete"))
        return format_html(' '.join([edit, delete]))

    class Meta:
        orderable = False
        fields = ('title', 'author', 'created', 'risk', 'event_type', 'tag', 'actions')
        model = Event
        template_name = 'django_tables2/bootstrap.html'
        attrs = {'id': 'BSdataTable', 
                 'class': 'table table-striped',
                 'cellspacing':'0',
                 'width':'100%'
            }
            
from django_filters.views import FilterView
from django_filters import FilterSet, ModelChoiceFilter
from django_tables2.views import SingleTableMixin

class EventFilter(FilterSet):
    tag = ModelChoiceFilter(queryset=Tag.objects.all())
    class Meta:
        model = Event
        fields = {
            'title': ['contains'],
            'tag': ['exact'],
            'type': ['exact'],
        }


class EventListView(UserCanViewDataMixin, SingleTableMixin, FilterView):
    context_object_name = 'events'
    paginate_by = 3
    template_name = 'events/event_list.html'
    model = Event
    table_class = EventTable
    filterset_class = EventFilter

    def get_context_data(self, **kwargs):
        tag = None
        context = super(EventListView, self).get_context_data(**kwargs)
        self.queryset = Event.published.all()

        return context


class EventCommentForm(forms.Form):
    message = forms.CharField()

class EventDisplay(DetailView):
    template_name = 'events/event_detail.html'
    model = Event
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super(EventDisplay, self).get_context_data(**kwargs)
        slug = kwargs['object'].slug
        event = get_object_or_404(Event, slug=slug,
                                   status='published')

        comments = event.event_comments.filter(active=True) 

        event_tag_ids = event.tag.values_list('id', flat=True)
        similar_events = Event.published.filter(tag__in=event_tag_ids).exclude(id=event.id)
        similar_events = similar_events.annotate(same_tags=Count('tag')).order_by('-same_tags',
                                                                             '-created')[:4]
        observables = event.observable.all()
        documents = event.event_document.all()

        threat_actors = event.threat_actor.all()
        context = {'event': event, 
                   'comments': comments,
                   'observables': observables,
                   'documents': documents,
                   'threat_actors': threat_actors,
                   'similar_events': similar_events
                  }

        initial = {'author': self.request.user}
        context['form'] = self.form_class(initial=initial)
        return context


class DeleteEventView(UserCanViewDataMixin, DeleteView):
    model = models.Event
    template_name_suffix = '_delete'
    success_url = reverse_lazy('event:event_list')

    def get_object(self, queryset=None):
        object = super(DeleteEventView, self).get_object()
        user = self.request.user
        if user.is_superuser:
            return object
        else:
            org = user.account.organization
            if org == object.account.organization and user.is_staff:
                return object
            raise PermissionDenied('Not allowed')


class EventComment(SingleObjectMixin, FormView):
    template_name = 'events/event_detail.html'
    form_class = CommentForm
    model = Event

    def post(self, request, *args, **kwargs):
        comment_form = self.form_class(request.POST) 
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        new_comment = comment_form.save(commit=False)
        # Assign the current event to the comment
        new_comment.event = self.object
        # Save the comment to the database
        new_comment.save()

        return super(EventComment, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('events:event_detail', kwargs={'uuid': self.kwargs['uuid'], 'slug': self.kwargs['slug']})

class EventDetailView(View):

    def get(self, request, *args, **kwargs):
        view = EventDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EventComment.as_view()
        return view(request, *args, **kwargs)


class NewEventView(UserCanViewDataMixin, CreateView):
    model = models.Event
    form_class = EventForm
    template_name = 'events/event_create.html'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        doc_formset = context['doc_formset']
        observables = context['observables']
        threat_actor = context['threat_actors']
        if doc_formset.is_valid() and observables.is_valid() and threat_actor.is_valid():
            self.object = form.save()
            form.instance = self.object
            doc_formset.save()
            observables.save()
            threat_actor.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


    def get_object(self, queryset=None):
        obj = super(EventEditView, self).get_object(queryset=queryset)
        return obj

    def get_success_url(self):
        return reverse('events:event_list')

    def get_form_kwargs(self):
        kwargs = super(NewEventView, self).get_form_kwargs()
        kwargs['user_id'] = self.request.user.pk
        return kwargs


    def get_context_data(self, **kwargs):
        context = super(NewEventView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['doc_formset'] = DocumentFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['observables'] = ObservablesFormSet(self.request.POST, instance=self.object)
            context['threat_actors'] = ThreatActorsFormSet(self.request.POST, instance=self.object)
        else:
            context['doc_formset'] = DocumentFormSet(instance=self.object)
            context['observables'] = ObservablesFormSet(instance=self.object)
            context['threat_actors'] = ThreatActorsFormSet(instance=self.object)
        return context



class EventEditView(UserCanViewDataMixin, UpdateView):
    model = models.Event
    form_class = EventForm
    template_name = 'events/event_create.html'
    is_update_view = True


    def form_valid(self, form):
        self.object = form.save(commit=False)
        context = self.get_context_data()
        doc_formset = context['doc_formset']
        observables = context['observables']
        threat_actor = context['threat_actors']

        if doc_formset.is_valid() and observables.is_valid() and threat_actor.is_valid():
            self.object = form.save()
            form.instance = self.object
            doc_formset.save()
            observables.save()
            threat_actor.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


    def get_object(self, queryset=None):
        obj = super(EventEditView, self).get_object(queryset=queryset)
        return obj

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super(EventEditView, self).get_form_kwargs()
        kwargs['event_id'] = self.object.id
        kwargs['is_update'] = self.is_update_view
        kwargs['user_id'] = self.request.user.pk
        return kwargs


    def get_context_data(self, **kwargs):
        context = super(EventEditView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['doc_formset'] = DocumentFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['observables'] = ObservablesFormSet(self.request.POST, instance=self.object)
            context['threat_actors'] = ThreatActorsFormSet(self.request.POST, instance=self.object)
        else:
            context['doc_formset'] = DocumentFormSet(instance=self.object)
            context['observables'] = ObservablesFormSet(instance=self.object)
            context['threat_actors'] = ThreatActorsFormSet(instance=self.object)
        return context



def event_share(request, post_id):
    # Retrieve post by id
    event = get_object_or_404(Event, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            event_url = request.build_absolute_uri(event.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], event.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(event.title, event_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'events/share.html', {'event': event,
                                                    'form': form,
                                                    'sent': sent})


# API views

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be added, viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer

class TypeViewSet(viewsets.ModelViewSet):
    queryset = models.Type.objects.all()
    serializer_class = serializers.TypeSerializer
