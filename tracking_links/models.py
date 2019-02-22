from __future__ import unicode_literals
import numpy
import numconv

from django.db import models


def generate_hash():
    """
    generates a random seven character string using [0-9A-Za-z]
    """
    while True:  # equivelent to do-while
        candidate_key = numconv.NumConv(62).int2str(
            numpy.random.randint(0, 3521614606208, dtype=numpy.int64)
        )
        if GenericLink.objects.filter(pk=candidate_key).count() < 1:
            return candidate_key


class GenericLink(models.Model):
    id = models.CharField(
        primary_key=True, editable=False,
        max_length=8, default=generate_hash
    )
    redirect = models.URLField(max_length=2084, unique=True)
    clicked = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "generic link"
        verbose_name_plural = "generic links"

    def __str__(self, ):
        return self.redirect

    def redirect_url(self, ):
        self.clicked += 1
        self.save()
        return self.redirect

