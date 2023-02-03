from django.contrib import admin

from api.models import Genre, Person, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_filter = ("duration",)


@admin.register(Genre)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ("title",)


@admin.register(Person)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")