from ajax_select import urls as ajax_select_urls
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.decorators.cache import cache_page

from rest_framework import routers
from graphene_django.views import GraphQLView
from .views import (
    AboutView,
    AreaViewSet,
    ContactView,
    ContentTypeViewSet,
    LinkToPopoloSourceViewSet,
    MembershipViewSet,
    OrganizationViewSet,
    PersonSearchListView,
    PersonView,
    PersonViewSet,
    PopoloSourceViewSet,
    PostViewSet,
)
from .sitemap import PersonSitemap

CACHE_SECS = 60 * 60 * 24


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'posts', PostViewSet)
router.register(r'areas', AreaViewSet)
router.register(r'contenttypes', ContentTypeViewSet)
router.register(r'linktopopolosource', LinkToPopoloSourceViewSet)
router.register(r'popolosource', PopoloSourceViewSet)

urlpatterns = [
    url('^$',
        cache_page(CACHE_SECS)(PersonSearchListView.as_view()),
        name='person_list'),
    url('^person/(?P<person_id>\d+)-(?P<name_slug>[\w-]+)',
        cache_page(CACHE_SECS)(PersonView.as_view()),
        name='person'),

    url(r'^about$', AboutView.as_view(), name='about'),
    url(r'^contact$', ContactView.as_view(), name='contact'),

    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^admin/', admin.site.urls),


    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^graphql', GraphQLView.as_view(graphiql=True)),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'persons': PersonSitemap}},
        name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DJANGO_DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
