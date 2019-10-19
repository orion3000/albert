from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView, DetailsView, ValidCard, GenerateCard


urlpatterns = {
    url(r'^auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^creditcard/$', CreateView.as_view(), name="create"),
    url(r'^creditcard/(?P<pk>[0-9]+)/$',
        DetailsView.as_view(), name="details"),
    url(r'^validatecard/$', ValidCard.as_view(), name="validate"),
    url(r'^gencard/$', GenerateCard.as_view(), name="generate"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
