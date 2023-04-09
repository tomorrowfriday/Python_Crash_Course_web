import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect, Http404
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """ Main page "watch gournal"."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Shows all Topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id = topic_id)
    #Ensure that topic was created by current user
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        #no data send; empty form created
        form = TopicForm()
    else:
        # send POST: work data.
        form = TopicForm(data = request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            form.save()

            #creating the folder on Desctop
            desktop_path = os.path.join(settings.HOME, 'Desktop')
            topic_folder_path = os.path.join(desktop_path, new_topic.text)
            os.makedirs(topic_folder_path)
            #
            return redirect('learning_logs:topics')

    # show empty or not valid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new Entry for a topic"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # No data sent
        form = EntryForm()
        context = {'topic': topic, 'form': form}
        return render(request, 'learning_logs/new_entry.html', context)
    else:
        # Recieved Data in POST-request; work out data.
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

        # Show invalid form with errors
        context = {'topic': topic, 'form': form}
        return render(request, 'learning_logs/new_entry.html', context)
    # Request method is not POST or GET, return 400 bad request
    return HttpResponseBadRequest()


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

    context = {'entry': entry, 'form': form, 'topic_id': topic.id}
    return render(request, 'learning_logs/edit_entry.html', context)
