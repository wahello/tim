b0VIM 7.4      kkZ�0 �	  gerd                                    gerd-LIFEBOOK-E544                      ~gerd/telescope/frontend/necti/views.py                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      utf-8 3210    #"! U                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 tp           _                            .       `                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      ad     �     _       �  �  V  5    �  �  �  �  �  j  \  >      �  �  �  �  �  k  3  2  �  �  �  �  �  G  $    �  �  W    �
  �
  �
  �
  �
  i
  U
  )
  (
  '
  �	  �	  �	  z	  B	  @	  	  �  �  �  a  _  :  �  �  �  ^  7    �  �  �  �  �  [    �  G  E  �  �  \         �  �  y  x  O    �  �  �  u  R      �  �  �                                  # Create Comment object but don't save to database yet             if comment_form.is_valid():              comment_form = CommentForm(data=request.POST)             # A comment was posted         if self.request.method == 'POST':         print comments         comments = object.event_comments.filter(active=True)         user = self.request.user         object = super(EventDetailView, self).get_object()     def get_object(self, queryset=None):      template_name = 'necti/event/event_detail.html'     model = Event class EventDetailView(UserCanViewDataMixin, generic.DetailView):  # #                                                     'similar_events': similar_events}) #                                                     'comment_form': comment_form, #                                                     'comments': comments, #    return render(request, 'necti/event/detail.html', {'event': event , # #                                                                             '-created')[:4] #    similar_events = similar_events.annotate(same_tags=Count('tag')).order_by('-same_tags', #    similar_events = Event.published.filter(tag__in=event_tag_ids).exclude(id=event.id) #    event_tag_ids = event.tag.values_list('id', flat=True) #    # List of similar posts # #        comment_form = CommentForm() #    else: #            new_comment.save() #            # Save the comment to the database #            new_comment.event = event #            #print help(new_comment) #            # Assign the current event to the comment #            new_comment = comment_form.save(commit=False) #            # Create Comment object but don't save to database yet #        if comment_form.is_valid(): # #        comment_form = CommentForm(data=request.POST) #        # A comment was posted #    if request.method == 'POST': #    comments = event.event_comments.filter(active=True) #    # List of active comments for this post # #                                   created__year=year) #                                   status='published', #    event = get_object_or_404(Event, slug=event, #    model = models.Event #def event_detail(request, year, event):       template_name = 'necti/event/list.html'     paginate_by = 3     context_object_name = 'events'     queryset = Event.published.all() class EventListView(ListView):                                                      'tag': tag})                                                    'events': events,     return render(request, 'necti/event/list.html', {'page': page,         events = paginator.page(paginator.num_pages)         # If page is out of range deliver last page of results     except EmptyPage:         events = paginator.page(1)         # If page is not an integer deliver the first page     except PageNotAnInteger:         events = paginator.page(page)     try:     page = request.GET.get('page')     paginator = Paginator(object_list, 3) # 3 posts in each page          object_list = object_list.filter(tag__in=[tag])         tag = get_object_or_404(Tag, slug=tag_slug)     if tag_slug:      tag = None     object_list = Event.published.all() def event_list(request, tag_slug=None):  from users.views import UserCanViewDataMixin from users.models import User import models from .forms import EmailPostForm, CommentForm, EventForm from .models import Event, EventComment  from taggit.models import Tag  from django.db.models import Count from django.core.mail import send_mail from django.views import generic from django.views.generic import ListView from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger from django.shortcuts import render, get_object_or_404 ad  :       .       �  �  ]  *    �  �  �  �  �  }  b  $  �  s    �  �  �  {  I    �  �  �  �  �  w  f  e  D  '  �
  �
  �
  �
  D
  �	  b	  	  	  �  �  �  Q                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      'sent': sent})                                                     'form': form,     return render(request, 'necti/event/share.html', {'event': event,         form = EmailPostForm()     else:             sent = True             send_mail(subject, message, 'admin@myblog.com', [cd['to']])             message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(event.title, event_url, cd['name'], cd['comments'])             subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], event.title)             event_url = request.build_absolute_uri(event.get_absolute_url())             cd = form.cleaned_data             # Form fields passed validation         if form.is_valid():         form = EmailPostForm(request.POST)         # Form was submitted     if request.method == 'POST':      sent = False     event = get_object_or_404(Event, id=post_id, status='published')     # Retrieve post by id def event_share(request, post_id):              return object                raise PermissionDenied('Not allowed')            if org != object.account.organization:            org = user.account.organization         else:                                                               #'similar_events': similar_events})                                                              #'comment_form': comment_form})                                                              'comments': comments,})             return render(self.request, 'necti/event/event_detail.html', {'object': object,             #return { 'object': object, 'comments':comments }             #return object             print object             print comments         if user.is_superuser:              comment_form = CommentForm()         else:                 new_comment.save()                 # Save the comment to the database                 new_comment.event = object                 # Assign the current event to the comment                 new_comment = comment_form.save(commit=False) 