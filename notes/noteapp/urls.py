from django.urls import path
from . import views
from .views import author_detail, note_list, note_detail
from .views import scrape_data_view

app_name = 'noteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('note/', views.note, name='note'),
    path('detail/<int:note_id>', views.detail, name='detail'),
    path('done/<int:note_id>', views.set_done, name='set_done'),
    path('delete-note/<int:id>/', views.delete_note, name='delete_note'),
    path('authors/', views.author_list, name='author_list'),
    path('add_author/', views.add_author, name='add_author'),
    path('delete_author/<int:author_id>/', views.delete_author, name='delete_author'),
    path('authors/<int:pk>/', author_detail, name='author_detail'),
    path('notes/', note_list, name='note_list'),
    path('notes/<int:pk>/', note_detail, name='note_detail'),
    path('notes/<int:id>/', views.note_detail, name='note_detail'),
    path('tag/<str:tag_name>/', views.tagged_notes, name='tagged_notes'),
    path('tag/<int:tag_id>/', views.notes_by_tag, name='notes_by_tag'),
    path('scrape/', scrape_data_view, name='scrape_data'),
]
