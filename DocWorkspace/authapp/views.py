from django.shortcuts import redirect

from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import CreateView
from django.urls import reverse

from .models import User
from .forms import RegistrationForm


class RegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm

    def get_context_data(self, *args, **kwargs):
        context = super(RegistrationView, self).get_context_data(*args, **kwargs)
        context['next'] = self.request.GET.get('next')
        return context

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        success_url = reverse('login')
        if next_url:
            success_url += '?next={}'.format(next_url)
        return success_url


class PasswordChangeView(PasswordChangeView):
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        meta_info = self.request.META.get('HTTP_REFERER').split('/')
        kwargs['user'] = User.objects.get(pk=meta_info[meta_info.index('user') + 1])
        return kwargs

def index(request):
    if request.user.is_anonymous:
        return redirect('login')
    if request.user.is_superuser:
        return redirect('admin/')
    if request.user.is_staff:
        return redirect('admin/')
    if request.user.kind.kind == 'D':
        return redirect('wards')
    return redirect('index')
