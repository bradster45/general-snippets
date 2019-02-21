# some useful Django queryset filtering using a datatime field

import datetime

from myapp.models import MyModel



# total count published since specific date - now
# total count / number of days

# 00:01 1/6/2018
d = datetime.datetime(2018, 6, 1, 00, 1)
now = datetime.datetime.now()
difference = now - d
days = difference.days
qs = MyModel.objects.filter(
    publication__gte=d,
    publication__lte=datetime.datetime.now()
)
count = qs.count()
per_day = (qs.count() / days)
print(count, per_day)
# (593, 2.3531746031746033)



# same thing but from 2 weeks ago, not specific date
days = (2 * 7)
qs = MyModel.objects.filter(
    publication__gte=datetime.datetime.now() - datetime.timedelta(days=days),
    publication__lte=datetime.datetime.now()
)
count = qs.count()
per_day = (qs.count() / days)
print(count, per_day)
# (35, 2.5)



# number published per date
days = (2 * 7)
now = datetime.datetime.now()

# sets todays time at 23:59, so query runs day1 23:59 - day2 23:59
# gives more accurate results than using whatever the time when running the query
todays_date = datetime.datetime(now.year, now.month, now.day, 23, 59)
# loop through days
for d in range(days):
    greater_than_date = todays_date - datetime.timedelta(days=(d + 1))
    less_than_date = todays_date - datetime.timedelta(days=d)
    qs = MyModel.objects.filter(
        publication__gte=greater_than_date,
        publication__lte=less_than_date
    )
    count = qs.count()
    print(less_than_date.date(), count)
    # 2019-01-31 5
    # 2019-01-30 7
    # 2019-01-29 7
    # ...



# number of objects published per day of the week
days_string = ['Sun', 'Mon', 'Tues', 'Weds', 'Thurs', 'Fri', 'Sat']
# last 4 weeks
days = (4 * 7)
for x in range(7):
    print('{}: {}'.format(
        days_string[x],
        MyModel.objects.filter(
            publication__gte=datetime.datetime.now() - datetime.timedelta(days=days),
            publication__lte=datetime.datetime.now(),
            publication__week_day=(x + 1)
        ).count()
    ))
    # Sun: 0
    # Mon: 17
    # Tues: 17
    # Weds: 15
    # Thurs: 11
    # Fri: 5
    # Sat: 0


