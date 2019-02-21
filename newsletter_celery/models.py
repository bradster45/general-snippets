from __future__ import unicode_literals

import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import lazy
from django.template.loader import render_to_string

from otherapp.models import Article


def get_base_templates():
    path = os.path.join(
        settings.BASE_DIR, 'public/templates/newsletter'
    )
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.isfile(os.path.join(path, 'default.html')):
        open(os.path.join(path, 'default.html'), 'w').close()
    return sorted([(t, t) for t in os.listdir(path)])


class Archtype(models.Model):
    title = models.CharField(max_length=256, unique=True, default='newsletter')
    users = models.ManyToManyField(
        User, through='Subscription',
        through_fields=('archtype', 'user'),
        related_name='archtypes'
    )
    template = models.CharField(choices=lazy(get_base_templates, tuple)())

    def __str__(self):
        return self.title


class Subscription(models.Model):
    archtype = models.ForeignKey(
        'Archtype', on_delete=models.CASCADE, related_name='subscriptions'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions'
    )
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            ('archtype', 'user', ),
        )

    def __str__(self):
        return '{} // {}'.format(self.user.username, self.archtype.title)


class Newsletter(models.Model):
    title = models.CharField(max_length=256, unique=True)
    STATES = (
        ('waiting', 'waiting'),
        ('paused', 'paused'),
        ('sending', 'sending'),
        ('finished', 'finished'),
    )
    users = models.ManyToManyField(
        User, through='Sent',
        through_fields=('newsletter', 'user'),
        related_name='newsletters'
    )
    state = models.CharField(choices=STATES, max_length=16, default='waiting')
    archtype = models.ForeignKey('Archtype', on_delete=models.CASCADE, related_name='newsletters')
    articles = models.ManyToManyField(
        Article, through='ArticleInNewsletter',
        through_fields=('newsletter', 'article'),
        related_name='article_in_newsletters'
    )
    scheduling = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def preview(self, user_id=False, email=False):
        #TODO:
        from app.tasks import send_mail
        send_mail(self.id, user_id, email, track=False)
        pass

    # states for sending emails with a periodic job, see settings and tasks
    def start(self, ):
        if self.state == 'waiting':
            self.state = 'sending'
            # clear all preview tracking info before sending
            Sent.objects.filter(newsletter=self).delete()
            from app.tasks import activate_emails
            activate_emails.delay()
            print('activate emails')
            self.save()
        return self.state

    def pause(self, ):
        if self.state == 'sending':
            self.state = 'paused'
            self.save()
        return self.state

    def resume(self, ):
        if self.state == 'paused':
            self.state = 'sending'
            self.save()
        return self.state

    # replace these two methods with annotations if used in a list
    def how_many_sent(self, ):
        return Sent.objects.filter(
            newsletter=self
        ).count()

    def to_html_string(self, context={}, request=None):
        context['articles'] = self.articles
        return render_to_string(
            'newsletter/' + self.archtype.template,
            context, request
        )


# tracking which users have had the newsletter sent
class Sent(models.Model):
    newsletter = models.ForeignKey(
        'Newsletter', on_delete=models.CASCADE, related_name='sent'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('newsletter', 'user', ),
        )


class ArticleInNewsletter(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='article_in_newsletters'
    )
    newsletter = models.ForeignKey(
        Newsletter, on_delete=models.CASCADE, related_name='article_in_newsletters'
    )

    class Meta:
        unique_together = (
            ('newsletter', 'article', ),
        )

    def __str__(self):
        return '{} // {}'.format(self.article.title, self.newsletter.title)


# user article tracking for newsletters/newsletters
class UserOfArticleInNewsletter(models.Model):
    article_in_newsletter = models.ForeignKey(
        ArticleInNewsletter, on_delete=models.CASCADE,
        related_name='users_of_article_in_newsletter',
        verbose_name='article in newsletters'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='users_of_article_in_newsletters',
        verbose_name='user'
    )

    class Meta:
        verbose_name = ('user of article in newsletter')
        verbose_name_plural = (
            'users of article in newsletters')
        unique_together = (
            ('article_in_newsletter', 'user', ),
        )

    def __str__(self):
        return '{} clicked {}'.format(
            self.user.user.username,
            self.article_in_newsletter.article.title
        )

