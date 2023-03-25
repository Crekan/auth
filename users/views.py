from django.shortcuts import render, redirect
from django.views import View

from .forms import CustomUserCreationForm


class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': CustomUserCreationForm(),
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

        context = {
            'form': form,
        }

        return render(request, self.template_name, context)
