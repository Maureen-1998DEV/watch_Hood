from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import UserProfile, Post, Neighborhood, Business, Comment
from django.contrib.auth.decorators import login_required
import datetime as dt
from .forms import UserProfileForm, BusinessForm, PostForm, CommentForm
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import BusinessSerializer
from .email import send_amber_email

# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            # check if user exists and if not set neighborhood to None
            if UserProfile.objects.filter(user_id=current_user.id).exists():
                profile = UserProfile.objects.get(user_id=current_user.id)
                post.neighborhood = profile.neighborhood
            else:
                post.neighborhood = 1
            post.type = request.POST['type']
            post.save()
        return redirect('index')
    else:
        form = PostForm()

    if UserProfile.objects.filter(user_id=current_user.id).exists():
        profile = UserProfile.objects.get(user_id=current_user.id)
        if profile.neighborhood:
            neighborhood = Neighborhood.objects.get(id=profile.neighborhood.id)
            posts = Post.objects.filter(neighborhood=neighborhood)
            businesses = Business.objects.filter(neighborhood=neighborhood)
            return render(request, 'index.html', {"posts": posts, "businesses": businesses, "profile": profile, "form": form})
        else:
            
            return render(request, 'index.html', {"profile": profile, "form": form})
    else:
        return render(request, 'index.html', {"form": form})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    date = dt.date.today()
    current_user = request.user
    profile = UserProfile.objects.objects.filter(
        user_id=current_user.id).first()
    posts = Post.objects.filter(user_id=current_user.id)
    if request.method == 'POST':
        signup_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('profile')
    else:
        signup_form = UserProfileForm()

    return render(request, 'profile/edit_profile.html', {"date": date, "form": signup_form, "profile": profile, "posts": posts})


def profile(request):
    date = dt.date.today()
    current_user = request.user
    profile = UserProfile.objects.get(user=current_user.id)
    posts = Post.objects.filter(user=current_user)
    return render(request, 'profile/profile.html', {"date": date, "profile": profile, "posts": posts})


@login_required(login_url='/accounts/login/')
def businesses(request):
    current_user = request.user
    neighborhood = UserProfile.objects.get(user=current_user).neighborhood
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.neighborhood = neighborhood
            business.save()
            return redirect('businesses')
    else:
        form = BusinessForm()

    try:
        businesses = Business.objects.filter(neighborhood=neighborhood)
    except:
        businesses = None

    return render(request, 'business.html', {"businesses": businesses, "form": form})


def post(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
        return redirect('post', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'post.html', {"post": post, "comments": comments, "form": form})


class BusinessList(APIView):
    def get(self, request, format=None):
        all_businesses = Business.objects.all()
        serializers = BusinessSerializer(all_businesses, many=True)
        return Response(serializers.data)


def search(request):
    current_user = request.user
    if 'search' in request.GET and request.GET["search"]:
        search_term = request.GET.get("search")
        businesses = Business.objects.filter(name__icontains=search_term)
        return render(request, 'search.html', {'businesses': businesses})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})