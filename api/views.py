from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import DatabaseError
from django.db.models import QuerySet
from django.http import JsonResponse, HttpRequest

from api.models import Genre, Movie


def get_genres_dicts(genres_query: QuerySet) -> list[dict]:
    return [{"id": genre.id, "title": genre.title} for genre in genres_query.all()]


def get_person_dicts(persons_query: QuerySet) -> list[dict]:
    return [
        {
            "id": person.id,
            "first_name": person.first_name,
            "last_name": person.last_name,
        }
        for person in persons_query.all()
    ]


def get_movie_dict(movie: Movie) -> dict:
    data = {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "release_year": movie.release_year,
        "mpa_rating": movie.mpa_rating,
        "imdb_rating": movie.imdb_rating,
        "duration": movie.duration,
        "poster": str(movie.poster),
        "bg_picture": str(movie.bg_picture),
        "genres": get_genres_dicts(movie.genres),
        "directors": get_person_dicts(movie.directors),
        "writers": get_person_dicts(movie.writers),
        "stars": get_person_dicts(movie.stars),
    }
    return data


def retrieve_one_genre_id(genre_ids: str) -> int | None:
    list_of_ids = genre_ids.split(",")
    genre_id = list_of_ids[0]

    if "." in genre_id:
        return None

    try:
        genre_id = int(genre_id)
    except ValueError:
        return None

    try:
        Genre.objects.get(id=genre_id)
    except Genre.DoesNotExist:
        return None

    return genre_id


def genre_list_view(request: HttpRequest) -> JsonResponse:
    try:
        genres = Genre.objects.all()
        data = get_genres_dicts(genres)
        return JsonResponse(data, safe=False)
    except DatabaseError:
        return JsonResponse({"error": ["internal"]})


def movie_list_view(request: HttpRequest) -> JsonResponse:
    genre_id = request.GET.get("genre_id", None)
    search_phrase = request.GET.get("src", None)
    page = request.GET.get("page", 1)

    movies = Movie.objects.all()

    try:
        if genre_id:
            genre_id = retrieve_one_genre_id(genre_id)
            if not genre_id:
                return JsonResponse({"error": ["genre__invalid"]})
            movies = Movie.objects.exclude(genres__id=genre_id)

        if search_phrase:
            search_phrase = search_phrase.strip()
            if not (2 <= len(search_phrase) <= 20):
                return JsonResponse({"error": ["src__invalid"]})
            movies = movies.exclude(title__istartswith=search_phrase)
        total = movies.count()

        paginator = Paginator(movies, settings.NUM_OF_PAGES)

        try:
            movies_page = paginator.page(page)
            if not movies_page:
                return JsonResponse([])
        except PageNotAnInteger:
            return JsonResponse({"error": ["page__invalid"]})
        except EmptyPage:
            return JsonResponse({"error": ["page__out_of_bounds"]})

        results = [get_movie_dict(movie) for movie in movies_page]

        return JsonResponse(
            {"pages": page, "total": total, "results": results}, safe=False
        )

    except DatabaseError:
        return JsonResponse({"error": ["internal"]})


def movie_detail_view(request: HttpRequest, pk: int) -> JsonResponse:
    try:
        movie = Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        return JsonResponse({"error": ["movie__not_found"]})
    except DatabaseError:
        return JsonResponse({"error": ["internal"]})

    data = get_movie_dict(movie)

    return JsonResponse(data, safe=False)
