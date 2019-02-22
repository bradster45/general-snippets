import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class AutoSluggedAbstractModel(models.Model):
    """
    unique title & slug. slug is generated from title
    if it's not otherwise provided
    """
    title = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, blank=True, default='', max_length=256)

    class Meta:
        abstract = True

    def __str__(self, ):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.title)
        super(AutoSluggedAbstractModel, self).save(*args, **kwargs)


class TimeStampedAbstractModel(models.Model):
    """
    timestamping created & updated datetimes
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TrackedAbstractModel(TimeStampedAbstractModel):
    """
    extends TimeStampedAbstractModel with references to the User model
    may need to set request.user as the initial value in the form
    """
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)ss_created', verbose_name='creator'
    )
    updater = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)ss_updated', verbose_name='updater'
    )

    class Meta:
        abstract = True


# as an example, Article will have the fields from all
# the abstract models as well as my own
class Article(AutoSluggedAbstractModel, TrackedAbstractModel):
    description = models.TextField(max_length=256)
