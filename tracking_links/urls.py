from django.conf.urls import url
from app.views import *

urlpatterns = [
    url(
        r'^(?P<pk>\w+)/$',
        GenericLinkRedirectView.as_view(),
        name='generic_link_redirect'
    ),
    # <a href="{% url ads:generic_link_redirect pk %}">...</a>
]
