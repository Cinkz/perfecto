from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/', include('account.urls')),
    url(r'^api/', include('authtoken.urls')),
    url(r'^api/', include('channel.urls')),
    url(r'^api/', include('dialogue.urls')),
    url(r'^api/', include('prototype.urls')),
    url(r'^api/', include('transaction.urls')),
]
