from django.urls import path

from api.views import genre_list_view, movie_list_view, movie_detail_view

urlpatterns = [
    path("genres/", genre_list_view, name="genres_list"),
    path("movies/", movie_list_view, name="movies_list"),
    path("movies/<int:pk>", movie_detail_view, name="movie_detail")
]

app_name = "api"
