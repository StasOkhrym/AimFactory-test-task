from decimal import Decimal

from django.test import TestCase

from api.models import Genre, Movie, Person


class ModelTests(TestCase):

    def test_genre_str(self):
        title = "Test"
        genre = Genre.objects.create(title=title)

        self.assertEqual(str(genre), title)

    def test_person_str(self):
        first_name = "TestName"
        last_name = "TestName"
        types = Person.PersonStatus.ACTOR

        check_string = f"{first_name} {last_name} (actor)"

        person = Person.objects.create(
            first_name=first_name,
            last_name=last_name,
            types=types
        )

        self.assertEqual(str(person), check_string)

    def test_movie_str(self):
        title = "Test"
        movie = Movie.objects.create(
            title=title,
            description="Test",
            release_year=2015,
            mpa_rating=Movie.MPARating.G,
            imdb_rating=Decimal("7.5"),
            duration=15
        )

        self.assertEqual(str(movie), title)
