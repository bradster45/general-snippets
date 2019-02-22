from django.views.generic import RedirectView

from app.models import GenericLink

class GenericLinkRedirectView(RedirectView):
    permanent = False
    def get_redirect_url(self, **kwargs):
        # The redirect_url method handles both counting and url generation
        return GenericLink.objects.get(
            pk=self.kwargs.get('pk')
        ).redirect_url()

