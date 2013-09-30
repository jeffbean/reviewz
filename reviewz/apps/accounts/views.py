# Create your views here.
from django.contrib.auth import get_user_model, logout
from django.http import HttpResponseRedirect
from django.views.generic import DetailView


class AccountProfileView(DetailView):
    model = get_user_model()

    def get(self, request, *args, **kwargs):
        pass

    def get_object(self, queryset=None):
        pass


def account_logout(request):
    logout(request)
    return HttpResponseRedirect('/')