from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('',views.index,name = 'index'),
    url('^profile/$',views.profile,name='profile'),
    url('^profiles/(\d+)',views.profile,name='profiles'),
    url('^edit/profile/$',views.edit_profile,name='edit_profile'),
    url('^businesses$',views.businesses,name = 'businesses'),
    url('^post/(?P<id>\d+)',views.post,name='post'),
    url('^search/$',views.search,name='search'),
    url('^api/businesses/$',views.BusinessList.as_view())

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)