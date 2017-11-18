from django.conf import settings
from django.conf.urls import url

from .views import BiPiView


urlpatterns = [
    url(r'^{}/$'.format(settings.TGRM_TOKEN[-35:]), BiPiView.as_view(), name='main'),
]
