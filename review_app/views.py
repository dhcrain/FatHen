from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import TemplateView, UpdateView, CreateView, DetailView, ListView
# from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from review_app.models import Profile, FarmersMarket, Vendor, VendorType, Rating
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

class FarmersMarketDetailView(DetailView):
    model = FarmersMarket
    slug_field = 'fm_slug'
    slug_url_kwarg = 'fm_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fm_slug = self.kwargs.get('fm_slug')
        mrkt = FarmersMarket.objects.get(fm_slug=fm_slug)
        context['vendor_list'] = Vendor.objects.filter(at_farmers_market__fm_slug=fm_slug)
        return context


class FarmersMarketCreateView(CreateView):
    model = FarmersMarket
    # success_url = reverse_lazy('farmers_market_detail_view')
    fields = ['fm_name', 'fm_description', 'fm_contact_name', 'fm_contact_email',
              'fm_website', 'fm_facility_type', 'fm_county', 'fm_address',
              'fm_programs_accepted', 'fm_phone', 'fm_hrs_of_operation',
              'fm_seasons_of_operation', 'fm_handicap_accessible', 'fm_picture', 'fm_banner_picture']

    def get_success_url(self):
        return reverse('farmers_market_detail_view',args=(self.object.fm_slug,))


class VendorDetailView(DetailView):
    model = Vendor
    slug_field = 'vendor_slug'
    slug_url_kwarg = 'vendor_slug'


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    fields = ['user_type', 'profile_picture']
    success_url = reverse_lazy("index_view")

    def get_object(self, queryset=None):
        return self.request.user.profile


class RegisterView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
