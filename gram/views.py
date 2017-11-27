from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.db import transaction

from .forms import UserForm, ProfileForm, PostForm
from .models import Post

from django.core.urlresolvers import reverse

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

            return redirect(reverse('user', kwargs={'username': request.user.username}))

    else:

        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profiles/profile.html', {

        'user_form': user_form,
        'profile_form': profile_form,
        'user': user
    })


def upload_post(request):

    if request.method == 'POST':

        form = PostForm(request.POST, files=request.FILES)

        if form.is_valid():

            single_post = Post(user=request.user, image=request.FILES['image'], caption=request.POST['caption'])

            single_post.save()

            return redirect(reverse('user', kwargs={'username': request.user.username}))

    else:

        form = PostForm()

        return render(request, 'base/upload-photo.html', {'form': form})


