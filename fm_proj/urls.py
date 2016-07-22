"""fm_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from review_app.views import IndexView, ProfileView, RegisterView, FarmersMarketListView, FarmersMarketDetailView, FarmersMarketCreateView, FarmersMarketUpdateView, VendorDetailView, VendorCreateView, VendorUpdateView, RatingVendorCreateView

urlpatterns = [
    url(r'^review/', include('review.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', IndexView.as_view(), name='index_view'),
    url(r'^register/$', RegisterView.as_view(), name='register_view'),
    url(r'^accounts/profile/$', ProfileView.as_view(), name='profile_view'),
    url(r'^farmers_markets/$', FarmersMarketListView.as_view(), name='farmers_market_list_view'),
    url(r'^farmers_markets/add/$', FarmersMarketCreateView.as_view(), name='farmers_market_create_view'),
    url(r'^fm/(?P<fm_slug>[A-Za-z0-9_\-]+)/$', FarmersMarketDetailView.as_view(), name='farmers_market_detail_view'),
    url(r'^fm/(?P<fm_slug>[A-Za-z0-9_\-]+)/update/$', FarmersMarketUpdateView.as_view(), name='farmers_market_update_view'),
    url(r'^vendor/add/$', VendorCreateView.as_view(), name='vendor_create_view'),
    url(r'^vendor/(?P<vendor_slug>[A-Za-z0-9_\-]+)/$', VendorDetailView.as_view(), name='vendor_detail_view'),
    url(r'^vendor/(?P<vendor_slug>[A-Za-z0-9_\-]+)/update$', VendorUpdateView.as_view(), name='vendor_update_view'),
    url(r'^vendor/(?P<vendor_slug>[A-Za-z0-9_\-]+)/rate$', RatingVendorCreateView.as_view(), name='rating_vendor_create_view'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
