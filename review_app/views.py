import datetime
import operator
import requests
import geocoder
import os
from functools import reduce
from django.db.models import Q
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView, DetailView, ListView
# from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from review_app.models import Profile, FarmersMarket, Vendor, VendorType, Rating, Status
from review_app.forms import StatusCreateForm
from review.templatetags.review_tags import total_review_average
from django.db.models import Case, When
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_form"] = AuthenticationForm()
        return context

class FarmersMarketListView(ListView):
    template_name = 'review_app/farmersmarkets_list.html'
    model = FarmersMarket
    paginate_by = 25

    def get_queryset(self, **kwargs):
        rated = self.request.GET.get('rated')
        sort = self.request.GET.get('sort')
        if sort:
            return FarmersMarket.objects.all().order_by(sort)
        elif rated:
            # http://stackoverflow.com/a/38390480/5119789
            reviews = [(total_review_average(market), market.pk) for market in FarmersMarket.objects.all()]
            pk_list = [mkt[1] for mkt in sorted(reviews, key=lambda x: x[0], reverse=True)]
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
            return FarmersMarket.objects.filter(pk__in=pk_list).order_by(preserved)
        else:
            return FarmersMarket.objects.all()



class FarmersMarketDetailView(DetailView):
    model = FarmersMarket
    slug_field = 'fm_slug'
    slug_url_kwarg = 'fm_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fm_slug = self.kwargs.get('fm_slug')
        sort = self.request.GET.get('sort')
        rated = self.request.GET.get('rated')
        forecast = self.request.GET.get('forecast')
        # if forecast:
        location = FarmersMarket.objects.get(fm_slug=fm_slug)
        g = geocoder.google(location.fm_address)

        api_key = os.environ['forecast_api']
        lat = g.latlng[0]
        lng = g.latlng[1]
        # current_time = datetime.datetime.now()
        print(api_key)
        url = "https://api.forecast.io/forecast/{}/{},{}".format(api_key, lat, lng)
        response = requests.get(url).json()
        context['forecast_summary'] = response['daily']['summary']
        context['forecast'] = response['daily']['data']

        if sort:
            context['vendor_list'] = Vendor.objects.filter(at_farmers_market__fm_slug=fm_slug).order_by(sort)
        elif rated:
            # http://stackoverflow.com/a/38390480/5119789
            reviews = [(total_review_average(vendor), vendor.pk) for vendor in Vendor.objects.all()]
            pk_list = [vendor[1] for vendor in sorted(reviews, key=lambda x: x[0], reverse=True)]
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
            context['vendor_list'] = Vendor.objects.filter(at_farmers_market__fm_slug=fm_slug).filter(pk__in=pk_list).order_by(preserved)
        else:
            context['vendor_list'] = Vendor.objects.filter(at_farmers_market__fm_slug=fm_slug)
        mrkt = FarmersMarket.objects.get(fm_slug=fm_slug)
        context['fm_status_form'] = StatusCreateForm()
        one_week = datetime.datetime.now() + datetime.timedelta(days=-7)
        context['status_list'] = Status.objects.filter(status_fm=mrkt).filter(status_created__gt=one_week)
        return context


class FarmersMarketStatusCreateView(CreateView):
    model = Status
    form_class = StatusCreateForm

    def form_valid(self, form, **kwargs):
        status_form = form.save(commit=False)
        fm_slug = self.kwargs.get('fm_slug')
        status_form.status_user = self.request.user
        status_form.status_fm = FarmersMarket.objects.get(fm_slug=fm_slug)
        return super().form_valid(form)

    def get_success_url(self):
        fm_slug = self.kwargs.get('fm_slug')
        return reverse('farmers_market_detail_view', args=(fm_slug,))


class FarmersMarketCreateView(CreateView):
    model = FarmersMarket
    fields = ['fm_name', 'fm_description', 'fm_contact_name', 'fm_contact_email',
              'fm_website', 'fm_facility_type', 'fm_county', 'fm_address',
              'fm_programs_accepted', 'fm_phone', 'fm_hrs_of_operation',
              'fm_seasons_of_operation', 'fm_handicap_accessible', 'fm_picture', 'fm_banner_picture']

    def get_success_url(self):
        return reverse('farmers_market_detail_view',args=(self.object.fm_slug,))


class FarmersMarketUpdateView(UpdateView):
    model = FarmersMarket
    slug_field = 'fm_slug'
    slug_url_kwarg = 'fm_slug'
    fields = ['fm_name', 'fm_description', 'fm_contact_name', 'fm_contact_email',
              'fm_website', 'fm_facility_type', 'fm_county', 'fm_address',
              'fm_programs_accepted', 'fm_phone', 'fm_hrs_of_operation',
              'fm_seasons_of_operation', 'fm_handicap_accessible', 'fm_picture', 'fm_banner_picture']

    def form_valid(self, form):
        fm_form = form.save(commit=False)
        fm_form.fm_user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('farmers_market_detail_view',args=(self.object.fm_slug,))


class VendorDetailView(DetailView):
    model = Vendor
    slug_field = 'vendor_slug'
    slug_url_kwarg = 'vendor_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vendor_slug = self.kwargs.get('vendor_slug')
        vendor = Vendor.objects.get(vendor_slug=vendor_slug)
        context['vendor_status_form'] = StatusCreateForm()
        context['status_list'] = Status.objects.filter(status_vendor=vendor)
        return context


class VendorStatusCreateView(CreateView):
    model = Status
    form_class = StatusCreateForm

    def form_valid(self, form, **kwargs):
        status_form = form.save(commit=False)
        vendor_slug = self.kwargs.get('vendor_slug')
        status_form.status_user = self.request.user
        status_form.status_vendor = Vendor.objects.get(vendor_slug=vendor_slug)
        return super().form_valid(form)

    def get_success_url(self):
        vendor_slug = self.kwargs.get('vendor_slug')
        return reverse('vendor_detail_view', args=(vendor_slug,))


class VendorCreateView(CreateView):
    model = Vendor
    slug_field = 'vendor_slug'
    slug_url_kwarg = 'vendor_slug'
    fields = ['at_farmers_market', 'vendor_name', 'vendor_description', 'vendor_contact_name',
              'vendor_contact_email', 'vendor_website', 'vendor_phone', 'vendor_type',
              'vendor_picture', 'vendor_banner_picture']

    def form_valid(self, form):
        vendor_form = form.save(commit=False)
        vendor_form.vendor_user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('vendor_detail_view',args=(self.object.vendor_slug,))


class VendorUpdateView(UpdateView):
    model = Vendor
    slug_field = 'vendor_slug'
    slug_url_kwarg = 'vendor_slug'
    fields = ['at_farmers_market', 'vendor_name', 'vendor_description', 'vendor_contact_name',
              'vendor_contact_email', 'vendor_website', 'vendor_phone', 'vendor_type',
              'vendor_picture', 'vendor_banner_picture']

    def form_valid(self, form):
        vendor_form = form.save(commit=False)
        vendor_form.vendor_user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('vendor_detail_view',args=(self.object.vendor_slug,))


class RatingVendorCreateView(CreateView):
    model = Rating
    fields = ['rating', 'rating_comment', 'rating_picture']

    def form_valid(self, form):
        vendor_review_form = form.save(commit=False)
        vendor_review_form.rating_user = self.request.user
        vendor_slug = self.kwargs.get('vendor_slug')
        vendor_review_form.rating_vendor = Vendor.objects.get(vendor_slug=vendor_slug)
        return super().form_valid(form)

    def get_success_url(self):
        vendor_slug = self.kwargs.get('vendor_slug')
        return reverse('vendor_detail_view',args=(vendor_slug,))


class StatusCreateView(CreateView):
    model = Status
    fields = ['status_vendor', 'status_fm', 'status_present', 'status_picture', 'status_comment']
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        status_form = form.save(commit=False)
        status_form.status_user = self.request.user
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    fields = ['user_type', 'profile_picture']
    success_url = reverse_lazy("index_view")

    def get_object(self, queryset=None):
        return self.request.user.profile


# modified from https://www.calazan.com/adding-basic-search-to-your-django-site/
class SearchListView(ListView):
    model = FarmersMarket
    paginate_by = 25

    def get_queryset(self):
        result = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_, (Q(fm_name__icontains=q) for q in query_list)) |
                reduce(operator.and_, (Q(fm_description__icontains=q) for q in query_list))
            )
        return result


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
