from django.contrib import admin

from words.word.models import Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ("original", "translation")
