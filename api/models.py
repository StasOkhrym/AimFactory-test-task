from enum import Enum
import os
import uuid as uuid
from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Person(models.Model):
    class PersonStatus(Enum):
        DIRECTOR = "director"
        WRITER = "writer"
        ACTOR = "actor"

    PERSON_STATUS_CHOICES = [(tag, tag.value) for tag in PersonStatus]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    types = models.CharField(choices=PERSON_STATUS_CHOICES, max_length=50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.types})"


def poster_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/posters/", filename)


def bg_picture_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/bg_pictures/", filename)


class Movie(models.Model):
    class MPARating(Enum):
        G = "G"
        PG = "PG"
        PG_13 = "PG-13"
        R = "R"
        NC_17 = "NC-17"

    MPA_RATING_CHOICES = [(tag, tag.value) for tag in MPARating]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    poster = models.ImageField(null=True, upload_to=poster_file_path)
    bg_picture = models.ImageField(null=True, upload_to=bg_picture_file_path)
    release_year = models.IntegerField()
    mpa_rating = models.CharField(choices=MPA_RATING_CHOICES, max_length=50)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=2)
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    directors = models.ManyToManyField(Person, related_name="movies_as_director")
    writers = models.ManyToManyField(Person, related_name="movies_as_writer")
    stars = models.ManyToManyField(Person, related_name="movies_as_star")

    def save(self, *args, **kwargs) -> None:
        persons = kwargs.pop("persons", None)
        if persons:
            for person in persons:
                status = person.types
                if status == Person.PersonStatus.DIRECTOR.value:
                    self.directors.add(person)
                if status == Person.PersonStatus.WRITER.value:
                    self.writers.add(person)
                if status == Person.PersonStatus.ACTOR.value:
                    self.stars.add(person)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
