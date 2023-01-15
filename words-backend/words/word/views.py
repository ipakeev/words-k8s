from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from words.word.models import Word


class WordListView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        words = Word.objects.values_list("original", flat=True)
        return render(request, "word/words.html", context={"words": words})
