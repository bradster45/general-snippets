# Newsletter celery

Example task using celery to queue and send a batch of emails.

#### Models
[Models](https://github.com/bradster45/general-snippets/blob/master/newsletter_celery/models.py) include simplified model structure needed to associate newsletters with Django user accounts, as well as relating articles to newsletter for embedding.

#### Settings
[Settings](https://github.com/bradster45/general-snippets/blob/master/newsletter_celery/settings.py) include the settings needed to periodically call the celery task from a Django project.

#### Tasks
[Tasks](https://github.com/bradster45/general-snippets/blob/master/newsletter_celery/tasks.py) have the python tasks responsible for figuring out which emails are still to be sent, and queuing them for sending.

#### Supervisor
[Supervisor](https://github.com/bradster45/general-snippets/blob/master/newsletter_celery/supervisor.conf) has a demo of how to setup the celery and celery beat servers. After making changes here, you need to run reread, update, and restart for the changed supervisor servers.
When starting the servers, the flow looks like this: project > project-celery > project-celery-beat
