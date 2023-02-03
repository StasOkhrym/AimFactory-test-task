from django.urls import path

from api.views import genres_list, movies_list, movie_by_id

urlpatterns = [
    path("genres/", genres_list, name="genres_list"),
    path("movies/", movies_list, name="movies_list"),
    path("movies/<int:pk>", movie_by_id, name="movie_detail")
]

app_name = "api"
