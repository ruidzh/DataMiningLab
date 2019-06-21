"""geodjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from taxi import views
from rest_framework import routers
from django.conf import settings
from xadmin.plugins import xversion
xversion.register_models()
import xadmin
xadmin.autodiscover()

router = routers.DefaultRouter()
router.register(r'trips', views.TripViewSet)
router.register(r'tripsets', views.TripsetViewSet)
router.register(r'districts', views.DistrictViewSet)
router.register(r'edges', views.EdgeViewSet)
router.register(r'matrixedges', views.MatrixEdgeViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('taxi.urls')),
    url(r'^rest/', include(router.urls)),
    url(r'xadmin/', include(xadmin.site.urls), name='xadmin'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns