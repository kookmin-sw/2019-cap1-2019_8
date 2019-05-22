import Dream.views as Dv
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^$', Dv.my_view, name='home'),
    url(r'^Dream/', include(('Dream.urls', 'Dream'), namespace='Dream')),
    url(r'^Dream/', Dv.clear_database, name='clear_database'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
