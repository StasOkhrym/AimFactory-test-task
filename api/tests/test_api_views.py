from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from api.models import Genre, Movie


class ViewsTests(TestCase):
    multi_db = True

    @classmethod
    def setUpClass(cls) -> None:
        Genre.objects.create(title="GenreTest")
        Genre.objects.create(title="TestName")
        Movie.objects.create(
            title="TitleTest",
            description="Test",
            release_year=2015,
            mpa_rating=Movie.MPARating.G,
            imdb_rating=Decimal("7.5"),
            duration=15,
        )

        Movie.objects.create(
            title="TestTitle",
            description="Test",
            release_year=2015,
            mpa_rating=Movie.MPARating.G,
            imdb_rating=Decimal("7.5"),
            duration=15,
        )

    @classmethod
    def tearDownClass(cls):
        Genre.objects.all().delete()
        Movie.objects.all().delete()

    def test_genre_list(self):
        check_data = [
            {"id": genre.id, "title": genre.title} for genre in Genre.objects.all()
        ]

        response = self.client.get(reverse("api:genres_list"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, check_data)

    def test_movie_details(self):
        response = self.client.get(reverse("api:movie_detail", args=[1]))

        check_data = {
            "id": 1,
            "title": "TitleTest",
            "description": "Test",
            "release_year": 2015,
            "mpa_rating": "G",
            "imdb_rating": "7.50",
            "duration": 15,
            "poster": "",
            "bg_picture": "",
            "genres": [],
            "directors": [],
            "writers": [],
            "stars": [],
        }

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, check_data)

    def test_movie_detail_does_not_exist(self):
        response = self.client.get(reverse("api:movie_detail", args=[5]))

        self.assertJSONEqual(response.content, {"error": ["movie__not_found"]})

    def test_movie_list(self):
        response = self.client.get(reverse("api:movies_list"))

        check_data = {
            "pages": 1,
            "total": 2,
            "results": [
                {
                    "id": 1,
                    "title": "TitleTest",
                    "description": "Test",
                    "release_year": 2015,
                    "mpa_rating": "G",
                    "imdb_rating": "7.50",
                    "duration": 15,
                    "poster": "",
                    "bg_picture": "",
                    "genres": [],
                    "directors": [],
                    "writers": [],
                    "stars": [],
                },
                {
                    "id": 2,
                    "title": "TestTitle",
                    "description": "Test",
                    "release_year": 2015,
                    "mpa_rating": "G",
                    "imdb_rating": "7.50",
                    "duration": 15,
                    "poster": "",
                    "bg_picture": "",
                    "genres": [],
                    "directors": [],
                    "writers": [],
                    "stars": [],
                },
            ],
        }

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, check_data)

    def test_page_not_exists(self):
        response = self.client.get(reverse("api:movies_list"), {"page": 5})

        self.assertJSONEqual(response.content, {"error": ["page__out_of_bounds"]})

    def test_invalid_page(self):
        response = self.client.get(reverse("api:movies_list"), {"page": "tests"})

        self.assertJSONEqual(response.content, {"error": ["page__invalid"]})

    def test_correct_filtering_by_src(self):
        response = self.client.get(reverse("api:movies_list"), {"src": "test"})

        check_data = {
            "pages": 1,
            "total": 1,
            "results": [
                {
                    "id": 1,
                    "title": "TitleTest",
                    "description": "Test",
                    "release_year": 2015,
                    "mpa_rating": "G",
                    "imdb_rating": "7.50",
                    "duration": 15,
                    "poster": "",
                    "bg_picture": "",
                    "genres": [],
                    "directors": [],
                    "writers": [],
                    "stars": [],
                }
            ],
        }

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, check_data)

    def test_invalid_src_short(self):
        response = self.client.get(reverse("api:movies_list"), {"src": "s"})

        self.assertJSONEqual(response.content, {"error": ["src__invalid"]})

    def test_invalid_src_long(self):
        response = self.client.get(
            reverse("api:movies_list"),
            {"src": "very_long_string_which_has_more_than_20_chars"},
        )

        self.assertJSONEqual(response.content, {"error": ["src__invalid"]})

    def test_filter_by_genre_id(self):
        movie1 = Movie.objects.get(id=1)
        movie2 = Movie.objects.get(id=2)

        genre1 = Genre.objects.get(id=1)
        genre2 = Genre.objects.get(id=2)

        movie1.genres.add(genre1)
        movie2.genres.add(genre2)

        movie1.save()
        movie2.save()

        response = self.client.get(reverse("api:movies_list"), {"genre_id": "1,2"})

        check_data = {
            "pages": 1,
            "total": 1,
            "results": [
                {
                    "id": 2,
                    "title": "TestTitle",
                    "description": "Test",
                    "release_year": 2015,
                    "mpa_rating": "G",
                    "imdb_rating": "7.50",
                    "duration": 15,
                    "poster": "",
                    "bg_picture": "",
                    "genres": [{"id": 2, "title": "TestName"}],
                    "directors": [],
                    "writers": [],
                    "stars": [],
                }
            ],
        }

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, check_data)

    def test_filter_when_genre_id_invalid_float(self):
        response = self.client.get(reverse("api:movies_list"), {"genre_id": "1.6,2"})

        self.assertJSONEqual(response.content, {"error": ["genre__invalid"]})

    def test_filter_when_genre_id_str(self):
        response = self.client.get(reverse("api:movies_list"), {"genre_id": "tests,2"})

        self.assertJSONEqual(response.content, {"error": ["genre__invalid"]})

    def test_filter_when_genre_id_does_not_exists(self):
        response = self.client.get(reverse("api:movies_list"), {"genre_id": "100,2"})

        self.assertJSONEqual(response.content, {"error": ["genre__invalid"]})
