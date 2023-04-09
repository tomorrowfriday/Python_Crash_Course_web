"""Defines URL patterns for learning_logs"""

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Main page
    path('', views.index, name='index'),
    # topics page
    path('topics/', views.topics, name='topics'),
    # page for a specific topics
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # new topic page
    path('new_topic/', views.new_topic, name = 'new_topic'),
    # page for a new EntryForm
    path('new_entry/<int:topic_id>/', views.new_entry, name = 'new_entry'),
    # page for editing entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name = 'edit_entry')
]
