from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout

from django.contrib.auth.models import User
from django.db import transaction

from .forms import UserForm, ProfileForm, PostForm, ProfPicForm, CommentForm
from .models import Post, Profile, Following, Comment, Like

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.http import Http404

# Create your views here.


@login_required(login_url='/accounts/login')
def index(request):

    title = 'Grammy Insta'

    following = Following.get_following(request.user)

    posts = Post.objects.filter().all().order_by('-id')

    return render(request, 'base/index.html', {'title': title, 'posts': posts, 'following': following})


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


def upload_photo(request, username):

    user = User.objects.get(username=username)

    if request.method == 'POST':

        form = PostForm(request.POST, files=request.FILES)

        if form.is_valid():

            single_post = form.save(commit=False)
            single_post.user = user
            single_post.save()

            return redirect(reverse('index'))

    else:

        form = PostForm()

        return render(request, 'base/upload-photo.html', {'form': form})


def profile(request, username):

    try:
        user = User.objects.get(username=username)

        profpic = Profile.objects.filter(user_id=user).all().order_by('-id')

        posts = Post.objects.filter(user_id=user).all().order_by('-id')

        following = Following.get_following(request.user)

    except ObjectDoesNotExist:
        raise Http404()

    return render(request, 'profiles/profile.html', {'user': user, 'posts': posts, 'profpic': profpic, 'following': following})


@transaction.atomic
def update_profile_pic(request, username):

    user = User.objects.get(username=username)

    if request.method == 'POST':

        form = ProfPicForm(request.POST, files=request.FILES)

        if form.is_valid():

            profile_picture = form.save(commit=False)
            profile_picture.user = user
            profile_picture.save()

            return redirect(reverse('profile', kwargs={'username': request.user.username}))

    else:

        form = ProfPicForm()

        return render(request, 'profiles/change-profpic.html', {'form': form})


def post(request, id):

    found_post = Post.objects.get(id=id)

    profpic = Profile.objects.get(user=request.user)

    reviews = Comment.objects.filter(post=found_post.id).order_by('-id')

    likes = Like.objects.filter(post=found_post.id)

    try:

        if request.method == 'POST':

            form = CommentForm(request.POST)

            if form.is_valid():

                review = form.save(commit=False)

                review.user = request.user

                review.post = found_post

                review.save()

                return redirect(post, found_post.id)

            else:

                form = CommentForm()

                return render(request, 'base/post.html', {'form': form, 'post': found_post,
                                                          'profpic': profpic, 'reviews': reviews,
                                                          'likes': likes})

        else:

            form = CommentForm()

            return render(request, 'base/post.html', {'form': form, 'post': found_post,
                                                      'profpic': profpic, 'reviews': reviews,
                                                      'likes': likes})

    except ObjectDoesNotExist:

        raise Http404


def search_results(request):

    if 'user' in request.GET and request.GET['user']:
        search_term = request.GET.get('user')
        searched_users = Profile.search_by_username(search_term)

        users = Profile.objects.filter(users= searched_users).all()

        return render(request, 'base/search-results.html', {"users": searched_users, 'users': users})

    else:
        message = "You haven't searched for any term"
        return render(request, 'base/search-results.html', {"message": message})


def explore(request):

    profiles = Profile.objects.filter(following=profile).order_by('-id')

    return render(request, 'base/explore.html', {'profiles': profiles})


def follow(request, id):

    follow_user = Profile.objects.get(id = id)

    following = Following(user=request.user, profile=follow_user)

    following.save()

    return redirect(explore)


def like(request, id):

    try:

        like_post = Post.objects.get(id=id)

        likes = Like(user=request.user, post=like_post, likes=1)

        likes.save()

        return redirect(index)

    except ObjectDoesNotExist:

        raise Http404()


# def comment(request, id):
#
#     single_post = Post.objects.get(id=id)
#
#     try:
#
#
#     except ObjectDoesNotExist:
#
#         raise Http404()









