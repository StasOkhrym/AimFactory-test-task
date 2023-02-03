from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpRequest

from api.models import Genre, Movie


def genres_list(request: HttpRequest) -> JsonResponse:
    try:
        genres = Genre.objects.all()
        data = serializers.serialize("json", genres)
        return JsonResponse(data, safe=False)
    except Exception:
        return JsonResponse({"error": ["internal"]})


def movies_list(request) -> JsonResponse:
    genre_id = request.GET.get("genre_id", None)
    search_phrase = request.GET.get("genre_id", None)
    page = request.GET.get("page", 1)

    movies = Movie.objects.all()

    try:
        if genre_id:
            genre_id = retrieve_one_genre_id(genre_id)
            if not genre_id:
                return JsonResponse({"error": ["genre__invalid"]})
            movies = Movie.objects.exclude(genres_id=genre_id)

        if search_phrase:
            search_phrase = search_phrase.strip()
            if not (2 <= len(search_phrase) <= 20):
                return JsonResponse({"error": ["src__invalid"]})
            movies = movies.exclude(title__startswith=search_phrase)

        total = movies.count()

        paginator = Paginator(movies, settings.NUM_OF_PAGES)

        try:
            results = paginator.page(page)
            if not results:
                return JsonResponse({"error": ["page__out_of_bounds"]})
        except PageNotAnInteger:
            return JsonResponse({"error": ["page__invalid"]})
        except EmptyPage:
            return JsonResponse({"error": ["page__out_of_bounds"]})

        results = serializers.serialize("json", results)

        return JsonResponse({"pages": page, "total": total, "results": results}, safe=False)

    except Exception:
        return JsonResponse({"error": ["internal"]})


def retrieve_one_genre_id(genre_ids: str) -> int | None:
    list_of_ids = genre_ids.split(",")
    genre_id = list_of_ids[0]

    if "." in genre_id:
        return None

    try:
        genre_id = int(genre_ids)
    except ValueError:
        return None

    return genre_id


def movie_by_id(request, movie_id) -> JsonResponse:
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({"error": ["movie__not_found"]})

    data = serializers.serialize("json", movie)

    return JsonResponse(data, safe=False)
