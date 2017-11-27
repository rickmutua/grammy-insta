from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.db import transaction

from .forms import UserForm, ProfileForm

# Create your views here.


@login_required(login_url='/accounts/login')
def index(request):

    title = 'Grammy Insta'

    return render(request, 'base/index.html', {'title': title })


@transaction.atomic
def update_profile(request, user_id):

    user = User.objects.get(pk=user_id)

    if request.method == 'POST':

        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            return redirect(request, 'profiles/profile.html', {'user': user})

    else:

        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profiles/profile.html', {

        'user_form': user_form,
        'profile_form': profile_form,
        'user': user
    })
