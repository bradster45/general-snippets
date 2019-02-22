# general-snippets

General snippets of code I thought were interesting

Contents:
- [Publication filters](https://github.com/bradster45/general-snippets/#publication-filters)
- [Newsletter engine](https://github.com/bradster45/general-snippets/#newsletter-engine)
- [Google recaptcha implimentation](https://github.com/bradster45/general-snippets/#google-recaptcha-implimentation)
- [Race simulation is JS](https://github.com/bradster45/general-snippets/#race-simulation-is-js)
- [Tracking links](https://github.com/bradster45/general-snippets/blob/master/datetime_filters.py)
- [Abstract models](https://github.com/bradster45/general-snippets/blob/master/datetime_filters.py)

### Publication filters

[Date filters](https://github.com/bradster45/general-snippets/blob/master/datetime_filters.py) are some useful examples of filtering using Django's DateTimeField. Examples include:
- Total count and count per day of objects from a provided date until the current date
- Total and per day count of objects from a set number of days ago to the current date
- Number of objects published per date from a set number of days ago to the current date
- Number of objects published per day from a set number of days ago to the current date

### Newsletter engine

[Newsletter engine](https://github.com/bradster45/general-snippets/tree/master/newsletter_celery) built with Python, using celery to queue periodic jobs.

### Google recaptcha implimentation

[Recaptcha](https://github.com/bradster45/general-snippets/blob/master/recaptcha.py) is how you can authenticate a user in a form using python requests and google recaptcha.

### Race simulation is JS

[Race simulator](https://github.com/bradster45/general-snippets/blob/master/race_simulation/race_reshuffle_demo.html) randomly generates lap times one by one and reshuffles a table of racers accordingly. Lap times are randomly generated until the final lap, at which point we see the final finish positions. See demo below.

![start](https://github.com/bradster45/general-snippets/blob/master/race_simulation/start.png)

![end](https://github.com/bradster45/general-snippets/blob/master/race_simulation/end.png)

Well done to racer 5.

### Tracking links

### Abstract models
