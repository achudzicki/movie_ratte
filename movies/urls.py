from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_movies, name='all_movies'),
    path('<int:id>', views.find_by_tmdb_id, name='movie'),
    path('filter', views.filter_movies),
    path('add', views.add_movie, name='add_movie'),
    path('collections', views.all_collections, name='all_collections'),
    path('collections/<int:id>', views.collection_details, name='collection')
]
