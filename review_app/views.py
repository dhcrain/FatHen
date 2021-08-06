import datetime
import operator
import requests
import geocoder
import os
from functools import reduce
from django.http import HttpResponseRedirect
from django.db.models import Case, When, Q
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
# from django.core.paginator import Paginator
# from django.core.mail import send_mail
# from fm_proj.settings import EMAIL_HOST_USER
from django.contrib.messages.views import SuccessMessageMixin
from review_app.tasks import contact_email
# from django.shortcuts import render
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import View, TemplateView, CreateView, DetailView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from review_app.models import Profile, FarmersMarket, Vendor, Status
from review_app.forms import StatusCreateForm, ContactForm, UserCreationEmailForm
from review.templatetags.review_tags import total_review_average
from review.forms import ReviewForm


class IndexView(ListView):
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        # http://stackoverflow.com/a/38390480/5119789
        reviews = [(total_review_average(market), market.pk)
                   for market in FarmersMarket.objects.all()]
        pk_list = [mkt[1]
                   for mkt in sorted(reviews, key=lambda x: x[0], reverse=True)]
        preserved = Case(*[When(pk=pk, then=pos)
                         for pos, pk in enumerate(pk_list)])
        # [:10]
        return FarmersMarket.objects.filter(pk__in=pk_list).order_by(preserved)

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
            reviews = [(total_review_average(market), market.pk)
                       for market in FarmersMarket.objects.all()]
            pk_list = [mkt[1] for mkt in sorted(
                reviews, key=lambda x: x[0], reverse=True)]
            preserved = Case(*[When(pk=pk, then=pos)
                             for pos, pk in enumerate(pk_list)])
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
        # forecast = self.request.GET.get('forecast')
        location = FarmersMarket.objects.get(fm_slug=fm_slug)
        api_key = os.environ['forecast_api']
        url = "https://api.forecast.io/forecast/{}/{},{}".format(
            api_key, location.fm_lat, location.fm_long)
        response = requests.get(url).json()
        if (location.fm_lat is not None or location.fm_long is not None):
            # weekly summary
            context['forecast_summary'] = response['daily']['summary']
            context['forecast_iframe_url'] = "https://forecast.io/embed/#lat={}&lon={}&name={}".format(
                location.fm_lat, location.fm_long, location.fm_name)
        if sort:
            context['vendor_list'] = Vendor.objects.filter(
                at_farmers_market__fm_slug=fm_slug).order_by(sort)
        elif rated:
            # http://stackoverflow.com/a/38390480/5119789
            reviews = [(total_review_average(vendor), vendor.pk)
                       for vendor in Vendor.objects.all()]
            pk_list = [vendor[1] for vendor in sorted(
                reviews, key=lambda x: x[0], reverse=True)]
            preserved = Case(*[When(pk=pk, then=pos)
                             for pos, pk in enumerate(pk_list)])
            context['vendor_list'] = Vendor.objects.filter(
                at_farmers_market__fm_slug=fm_slug).filter(pk__in=pk_list).order_by(preserved)
        else:
            context['vendor_list_present'] = Vendor.objects.prefetch_related('status_set').filter(
                at_farmers_market__fm_slug=fm_slug, status__status_present="Yes").distinct()
            context['vendor_list_no'] = Vendor.objects.prefetch_related('status_set').filter(
                at_farmers_market__fm_slug=fm_slug, status__status_present="No").distinct()
            context['vendor_list_nr_status'] = Vendor.objects.prefetch_related('status_set').filter(
                at_farmers_market__fm_slug=fm_slug, status__status_present="No Response").distinct()
            context['vendor_list_nr'] = Vendor.objects.prefetch_related('status_set').filter(
                at_farmers_market__fm_slug=fm_slug, status__status_present=None).distinct()
            context['vendor_list'] = Vendor.objects.prefetch_related('status_set').filter(
                at_farmers_market__fm_slug=fm_slug)  # .order_by('status')
        mrkt = FarmersMarket.objects.get(fm_slug=fm_slug)
        google_api = os.environ['google_maps_api']
        map_url = "https://www.google.com/maps/embed/v1/place?key={}&q={}".format(
            google_api, mrkt.fm_address)
        context['google_map'] = map_url
        context['fm_status_form'] = StatusCreateForm()
        context['review_form'] = ReviewForm(mrkt)
        """
        removed one_week filter for demo purposes
        one_week = datetime.datetime.now() + datetime.timedelta(days=-7)
        """
        context['status_list'] = Status.objects.filter(
            status_fm=mrkt)  # .filter(status_created__gt=one_week)
        context['num_likes'] = location.fm_likes.count()
        context['asdf'] = User.objects.get(
            username='asdf')  # default 'owner' of all fm/v
        return context


class FarmersMarketStatusCreateView(LoginRequiredMixin, CreateView):
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


class FarmersMarketCreateView(LoginRequiredMixin, CreateView):
    model = FarmersMarket
    fields = ['fm_name', 'fm_description', 'fm_contact_name', 'fm_contact_email',
              'fm_website', 'fm_facility_type', 'fm_county', 'fm_address',
              'fm_programs_accepted', 'fm_phone', 'fm_hrs_of_operation',
              'fm_seasons_of_operation', 'fm_handicap_accessible', 'fm_picture', 'fm_banner_picture']

    def form_valid(self, form):
        fm_form = form.save(commit=False)
        fm_form.fm_user = self.request.user
        fm_address = form.cleaned_data['fm_address']
        g = geocoder.google(fm_address)
        fm_form.fm_lat = g.latlng[0]
        fm_form.fm_long = g.latlng[1]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('farmers_market_detail_view', args=(self.object.fm_slug,))


class FarmersMarketUpdateView(LoginRequiredMixin, UpdateView):
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
        fm_address = form.cleaned_data['fm_address']
        g = geocoder.google(fm_address)
        fm_form.fm_lat = g.latlng[0]
        fm_form.fm_long = g.latlng[1]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('farmers_market_detail_view', args=(self.object.fm_slug,))


class ProfileFMLikeUpdateView(LoginRequiredMixin, View):

    def post(self, request, fm_slug, pk):
        fm_like = self.request.POST.get('fm_like')
        profile = Profile.objects.get(id=pk)
        if fm_like == 'Favorite':
            profile.profile_fm_like.add(
                FarmersMarket.objects.get(fm_slug=fm_slug))
        else:
            profile.profile_fm_like.remove(
                FarmersMarket.objects.get(fm_slug=fm_slug))
        return HttpResponseRedirect(reverse('farmers_market_detail_view', args=(fm_slug,)))


class ProfileVendorLikeView(LoginRequiredMixin, View):

    def post(self, request, vendor_slug, pk):
        vendor_like = self.request.POST.get('vendor_like')
        profile = Profile.objects.get(id=pk)
        if vendor_like == 'Favorite':
            profile.profile_vendor_like.add(
                Vendor.objects.get(vendor_slug=vendor_slug))
        else:
            profile.profile_vendor_like.remove(
                Vendor.objects.get(vendor_slug=vendor_slug))
        return HttpResponseRedirect(reverse('vendor_detail_view', args=(vendor_slug,)))


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
        context['review_form'] = ReviewForm(vendor)
        context['num_likes'] = vendor.vendor_likes.count()
        context['asdf'] = User.objects.get(
            username='asdf')  # default 'owner' of all fm/v
        return context


class VendorStatusCreateView(LoginRequiredMixin, CreateView):
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


class VendorCreateView(LoginRequiredMixin, CreateView):
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
        return reverse('vendor_detail_view', args=(self.object.vendor_slug,))


class VendorUpdateView(LoginRequiredMixin, UpdateView):
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
        return reverse('vendor_detail_view', args=(self.object.vendor_slug,))


class VendorDeleteView(LoginRequiredMixin, DeleteView):
    model = Vendor
    slug_field = 'vendor_slug'
    slug_url_kwarg = 'vendor_slug'
    success_url = reverse_lazy('index_view')

    def get_object(self, queryset=None):
        vendor = super().get_object()
        if not vendor.vendor_user == self.request.user:
            raise Http404
        return vendor


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ['status_vendor', 'status_fm',
              'status_present', 'status_picture', 'status_comment']
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        status_form = form.save(commit=False)
        status_form.status_user = self.request.user
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("index_view")

    def get_queryset(self):
        return Status.objects.filter(status_user=self.request.user)

    def get_success_url(self):
        return self.object.get_status_object.get_absolute_url()


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    fields = ['user_type', 'profile_picture']
    success_url = reverse_lazy('profile_view')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(profile_user=self.request.user)
        fm_favs = profile.profile_fm_like.all()
        vendor_favs = profile.profile_vendor_like.all()
        """
        removed one_week filter for demo purposes
        one_week = datetime.datetime.now() + datetime.timedelta(days=-7)
        """
        context['status_list'] = Status.objects.filter(Q(status_vendor__in=vendor_favs) | Q(
            status_fm__in=fm_favs))  # .filter(status_created__gt=one_week)
        return context


# modified from https://www.calazan.com/adding-basic-search-to-your-django-site/
class SearchListView(ListView):
    model = FarmersMarket
    paginate_by = 25

    def get_queryset(self):
        result = super().get_queryset()
        query = self.request.GET.get('q')
        search_type = self.request.GET.get('search_type')
        print(search_type)
        if query:
            query_list = query.split()
            if search_type == 'fm_name':
                result = result.filter(
                    reduce(operator.and_, (Q(fm_name__icontains=q) for q in query_list)))
            if search_type == 'fm_address':
                result = result.filter(
                    reduce(operator.and_, (Q(fm_address__icontains=q) for q in query_list)))
            if search_type == 'fm_programs_accepted':
                result = result.filter(reduce(
                    operator.and_, (Q(fm_programs_accepted__icontains=q) for q in query_list)))
        return result


class ContactView(SuccessMessageMixin, FormView):
    form_class = ContactForm
    template_name = 'review_app/contact.html'
    success_url = reverse_lazy('contact_view')
    success_message = "Thank you %(name)s, we will be in touch shortly"

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        from_email = form.cleaned_data.get('email')
        user = self.request.user
        form_message = form.cleaned_data.get('message')
        subject = form.cleaned_data.get('subject').strip()
        from_email = form.cleaned_data.get('email')
        # This is used to send the email with Celery delay
        contact_email(name, from_email, user, form_message, subject)
        return super().form_valid(form)


class AboutTemplateView(TemplateView):
    template_name = "about.html"


class RegisterView(CreateView):
    model = User
    form_class = UserCreationEmailForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # we are using email as username so let's copy it also to email field
        user = form.save(commit=False)
        user.email = user.username
        user.save()
        return super().form_valid(form)
