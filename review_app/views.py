from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'profile.html'
    fields = ['user_type', 'profile_picture']
    success_url = reverse_lazy("index_view")

    def get_object(self, queryset=None):
        return self.request.user.profile
