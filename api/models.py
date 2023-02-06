from django.db import models

from api.utils import bg_picture_file_path, poster_file_path


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class Genre(TimeStampModel):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Person(TimeStampModel):
    class PersonStatus(models.TextChoices):
        DIRECTOR = "director"
        WRITER = "writer"
        ACTOR = "actor"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    types = models.CharField(choices=PersonStatus.choices, max_length=50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.types})"


class Movie(TimeStampModel):
    class MPARating(models.TextChoices):
        G = "G"
        PG = "PG"
        PG_13 = "PG-13"
        R = "R"
        NC_17 = "NC-17"

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=5000)
    poster = models.ImageField(null=True, blank=True, upload_to=poster_file_path)
    bg_picture = models.ImageField(
        null=True, blank=True, upload_to=bg_picture_file_path
    )
    release_year = models.IntegerField()
    mpa_rating = models.CharField(choices=MPARating.choices, max_length=50)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=2)
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="movies")
    directors = models.ManyToManyField(Person, related_name="movies_as_director")
    writers = models.ManyToManyField(Person, related_name="movies_as_writer")
    stars = models.ManyToManyField(Person, related_name="movies_as_star")

    def __str__(self) -> str:
        return self.title
