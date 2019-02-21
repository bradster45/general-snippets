from celery import shared_task
from app.models import *

from django.core.mail import EmailMessage
from django.conf import settings
import datetime
from django.db.models import Q


@shared_task
def send_mail(newsletter, user):

    # assemble mail, send, create Sent object for user
    context = {}
    subject = newsletter.title

    # get user's email
    to_email = user.user.email

    # for unsubscribe link
    context['user_pk'] = user.pk

    body = newsletter.to_html_string(context)

    # construct the actual message, and send
    email_message = EmailMessage(
        subject,
        body,
        settings.EMAIL_FROM,
        [to_email]
    )
    email_message.content_subtype = 'html'
    email_message.send()

    return (to_email, str(datetime.datetime.now())[:19], newsletter.pk)


@shared_task
def activate_emails():
    for newsletter in Newsletter.objects.filter(Q(scheduling=None) | Q(scheduling__lte=datetime.datetime.now()), state='sending'):
        sent_count = Sent.objects.filter(newsletter=newsletter).count()
        subscriptions_count = newsletter.archtype.subscriptions.filter(active=True).count()
        if sent_count < subscriptions_count:
            for subscription in newsletter.archtype.subscriptions.filter(active=True).exclude(user__sent__newsletter=newsletter):
                if (newsletter.archtype.has_daily_limit and newsletter.daily_limit > sent_count) or not newsletter.archtype.has_daily_limit:
                    send_mail.delay(newsletter, subscription.user)
                    # MARK EMAIL AS SENT WHEN QUEUED, DON'T WAIT UNTIL IT'S SENT, OR IT WILL BE QUEUED MULTIPLE TIMES
                    Sent.objects.get_or_create(newsletter=newsletter, user=subscription.user)
                    sent_count += 1
                else:
                    break
        else:
            newsletter.state = 'finished'
            newsletter.save()
