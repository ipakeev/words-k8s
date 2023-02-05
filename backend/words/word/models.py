from django.db import models


class Word(models.Model):
    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"

    original = models.CharField(max_length=128, verbose_name="Оригинал")
    translation = models.CharField(
        max_length=128, blank=True, default="", verbose_name="Перевод"
    )

    def __str__(self) -> str:
        return self.original
