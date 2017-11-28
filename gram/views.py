from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout

from django.contrib.auth.models import User
from django.db import transaction

from .forms import UserForm, ProfileForm, PostForm, ProfPicForm
from .models import Post, Profile

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.http import Http404

# Create your views here.


@login_required(login_url='/accounts/login')
def index(request):

    title = 'Grammy Insta'

    posts = Post.objects.filter().all().order_by('-id')

    return render(request, 'base/index.html', {'title': title, 'posts': posts })


@transaction.atomic
def update_profile(request, username):

    user = User.objects.get(username = username)

    if request.method == 'POST':

        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            return redirect(reverse('profile', kwargs={'username': request.user.username}))

    else:

        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profiles/update-profile.html', {

        'user_form': user_form,
        'profile_form': profile_form,
        'user': user
    })


def upload_photo(request):

    if request.method == 'POST':

        form = PostForm(request.POST, files=request.FILES)

        if form.is_valid():

            single_post = Post(profile=request.user.profile, image=request.FILES['image'],
                               caption=request.POST['caption'])

            single_post.save()

            return redirect(reverse('upload-photo', kwargs={'username': request.user.username}))

    else:

        form = PostForm()

        return render(request, 'base/upload-photo.html', {'form': form})


def profile(request, username):

    try:
        user = User.objects.get(username=username)

        profpic = Profile.objects.filter(user_id=user).all().order_by('-id')

        posts = Post.objects.filter(user_id=user).all().order_by('-id')

    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'profiles/profile.html', {'user': user, 'posts': posts, 'profpic': profpic})


def update_profpic(request, username):

        user = User.objects.get(username=username)

        if request.method == 'POST':

            form = ProfPicForm(request.POST, files=request.FILES)

            if form.is_valid():

                profile_picture = Profile(profile=request.user.profile, profpic=request.FILES['profpic'])

                profile_picture.save()

                return redirect(reverse('profile', kwargs={'username': request.user.username}))

        else:

            form = ProfPicForm()

            return render(request, 'profiles/change-profpic.html', {'form': form})