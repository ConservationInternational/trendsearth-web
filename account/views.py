from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse
)
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission, User
from django.urls import reverse_lazy
from django.shortcuts import render
from django.template import loader
from django.contrib.auth import (
    login,
    authenticate,
    logout
)
from django.views.generic.edit import FormView
from django.contrib import messages

from account import models
from . import forms

from utils.api import (Api, RequestTask)


def signout(request):
    """Logout an active session

    Args:
        request (request): http request

    Returns:
        HttpResponse: If session is active, log out and redirect the view to home page
    """
    logout(request)
    if "bearer_token" in request.session:
        del request.session['bearer_token']

    return HttpResponseRedirect(reverse_lazy('login'))


class LoginView(FormView):
    """Renders to the login view

    Returns:
        HTTP Response: HTML content with the login view
    """

    form_class = forms.LoginForm
    success_url = reverse_lazy('dashboard')
    template_name = 'account/index.html'

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None and not user.profile.deleted:
            login(self.request, user)

            api = Api(username=credentials['email'],
                      password=credentials['password'])

            self.request.session['bearer_token'] = api.token

            if 'next' in self.request.POST:
                return HttpResponseRedirect(self.request.POST['next'])
            else:
                return HttpResponseRedirect(self.success_url)
        else:
            messages.add_message(self.request, messages.ERROR,
                                 'Wrong credentials please try again')
            return HttpResponseRedirect(reverse_lazy('login'))


@login_required
def view_profile(request):
    """Load logged in user profile view
    """
    template = loader.get_template('account/profile_detail.html')
    context = {
        'user': request.user
    }
    return HttpResponse(template.render(context, request))


@login_required
def register_user(request):
    """Create a new user

    Args:
        request (object): HTTP request

    Returns:
        [type]: [description]
    """

    if request.user.is_superuser:
        if request.method == 'POST':
            form = forms.SignupForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()

                user.profile.country_id = int(request.POST.get("country"))
                user.profile.region_id = int(request.POST.get("region"))
                user.profile.organization = request.POST.get("organization")

                user.profile.save()

                api = Api()
                api.register(email=user.email,
                             password=request.POST.get("password1"),
                             name=user.first_name + " " + user.last_name,
                             organization=user.profile.organization,
                             country=user.profile.country.name)

                return JsonResponse({"msg": "New user successfully added!"})
            else:
                messages.add_message(request, messages.ERROR,
                                     'Registration failed!')
        form = forms.SignupForm()
        template = loader.get_template('account/add_user.html')
        context = {
            'form': form,
            'countries': models.Country.objects.filter()
        }
        return HttpResponse(template.render(context, request))
    else:
        success_url = reverse_lazy('dashboard')
        return HttpResponseRedirect(success_url)
