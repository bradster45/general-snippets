from celery import shared_task
from app.models import *

from django.core.mail import EmailMessage
from django.conf import settings
import datetime
from django.db.models import Q


@shared_task
def send_mail(newsletter_id, user_id=False, email=False, track=True):

    # assemble mail, send, create Sent object for user
    context = {}
    newsletter = Newsletter.objects.get(pk=newsletter_id)
    subject = newsletter.title

    # if user_id, we get the user, and send to that user's email
    if user_id:

        user = User.objects.get(id=user_id)
        to_email = user.user.email

        # for unsubscribe link
        context['user_pk'] = user_id

    # else, and if email provided, send to that email
    elif email:

        to_email = email

        # if no user passed, use first user so click links don't throw an error
        context['user_pk'] = User.objects.first().pk

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

    # if track and user id provided, create the sent object
    if track and user_id:
        Sent.objects.get_or_create(newsletter=newsletter, user=user)
    return (to_email, str(datetime.datetime.now())[:19], newsletter.pk)


@shared_task
def activate_emails():
    for newsletter in Newsletter.objects.filter(Q(scheduling=None) | Q(scheduling__lte=datetime.datetime.now()), state='sending'):
        sent_count = Sent.objects.filter(newsletter=newsletter).count()
        subscriptions_count = newsletter.archtype.subscriptions.filter(active=True).count()
        if sent_count < subscriptions_count:
            for subscription in newsletter.archtype.subscriptions.filter(active=True).exclude(user__sent__newsletter=newsletter):
                if (newsletter.archtype.has_daily_limit and newsletter.daily_limit > sent_count) or not newsletter.archtype.has_daily_limit:
                    send_mail.delay(newsletter.id, subscription.user.id)
                    # MARK EMAIL AS SENT WHEN QUEUED, DON'T WAIT UNTIL IT'S SENT, OR IT WILL BE QUEUED MULTIPLE TIMES
                    Sent.objects.get_or_create(newsletter=newsletter, user=user)
                    sent_count += 1
                else:
                    break
        else:
            newsletter.state = 'finished'
            newsletter.save()
