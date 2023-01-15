from django.urls import path

from words.word.views import WordListView

app_name = "word"

urlpatterns = [
    path("", WordListView.as_view(), name="list")
]
