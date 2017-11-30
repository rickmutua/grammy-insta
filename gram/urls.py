from django.conf.urls import url
from . import views

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload-photo/(?P<username>[-_\w.]+)$', views.upload_photo, name='upload-photo'),
    url(r'^profile/(?P<username>[-_\w.]+)$', views.profile, name='profile'),
    url(r'^update-profile/(?P<username>[-_\w.]+)$', views.update_profile, name='update-profile'),
    url(r'^update-profile-picture/(?P<username>[-_\w.]+)$', views.update_profile_pic, name='update-profpic'),

    url(r'^post/(\d+)$', views.post, name='post'),

    url(r'^search/', views.search_results, name='search_results'),

    url(r'^logout/$', logout, {'index': settings.LOGOUT_REDIRECT_URL}, name='logout')
]


if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)