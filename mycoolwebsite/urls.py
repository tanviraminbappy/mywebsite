from django.conf.urls import url
from . import views
from django.contrib.sitemaps.views import sitemap
from mycoolwebsite.sitemaps import PostSitemap
from .feeds import LatestPostsFeed

sitemaps = {
        'posts' : PostSitemap
}

urlpatterns = [
        url(r'^$', views.post_list, name='post_list'),
        # url(r'^$', views.PostListView.as_view(), name='post_list' ),
        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail, name='post_detail'),
        url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
        url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
        url(r'^feed/$', LatestPostsFeed(), name='post_feed'),
]
