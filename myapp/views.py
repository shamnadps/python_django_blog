from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post,SalesTrackerUser,UserLocation
from .forms import PostForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapp.utils.messages import USER_ALREADY_EXISTS, ERROR_RESP, USER_CREATED, NOT_REGISTERED
# Create your views here.


def post_list(request):
    request.session['new'] = ''
    request.session['saved'] = ''
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    newItem = request.session.get('new')
    if not newItem:
        newItem = ''
    savedItem = request.session.get('saved')
    if not savedItem:
        savedItem = ''
    return render(request, 'blog/post_detail.html', {'post': post,'savedItem':savedItem,'newItem':newItem})

def post_new(request):
    request.session['new'] = ''
    request.session['saved'] = ''
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            users = User.objects.all()
            post.author = users[0]
            post.published_date = timezone.now()
            post.save()
            request.session['new'] = post.title
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    request.session['new'] = ''
    request.session['saved']=''
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            users = User.objects.all()
            post.author = users[0]
            post.published_date = timezone.now()
            post.save()
            request.session['saved'] = post.title
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    deletedItem = post.title
    post.delete()
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    return render(request, 'blog/post_list.html', {'posts': posts,'deletedItem':deletedItem})

@api_view(['GET', 'POST', ])
def user_regist(request):
    """
    :param request:
    :param format:
    :return:
    """
    username = request.GET.get('user', None)
    password = request.GET.get('pass', None)
    phone = request.GET.get('phone', None)
    if SalesTrackerUser.objects.filter(phone=phone).exists():
        ERROR_RESP['error']['message'] = USER_ALREADY_EXISTS
        return Response(status=status.HTTP_409_CONFLICT, data=ERROR_RESP)
    else:

        user = SalesTrackerUser(phone,username,password, phone, timezone.now(), 'true');
        user.created_date = timezone.now();
        user.save();

    # Building the response
    USER_CREATED['data']['username'] = username
    USER_CREATED['data']['phone'] = phone
    users = SalesTrackerUser.objects.filter(created_date__lte=timezone.now()).values()
    return Response(status=status.HTTP_201_CREATED, data=users)
	
@api_view(['GET', 'POST', ])
def checkphone(request):
    phonenumber = request.GET.get('phone', None)
    if SalesTrackerUser.objects.filter(phone=phonenumber).exists():
        user = SalesTrackerUser.objects.filter(phone=phonenumber).values()
        return Response(status=status.HTTP_201_CREATED, data=user)
    else:
        ERROR_RESP['error']['message'] = NOT_REGISTERED
        return Response(status=status.HTTP_409_CONFLICT, data=ERROR_RESP)
		
	
@api_view(['GET', 'POST', ])
def getuserlocation(request):
    phonenumber = request.GET.get('phonenumber', None)
    userlocations = SalesTrackerUser.objects.filter(phone=phonenumber).values()
    return Response(status=status.HTTP_201_CREATED, data=userlocations)
	
@api_view(['GET', 'POST', ])
def saveuserlocation(request):
    phonenumber = request.GET.get('phonenumber', None)
    latitude = request.GET.get('latitude', None)
    longitude = request.GET.get('longitude', None)
    userlocation = UserLocation(phone,latitude,longitude,timezone.now());
    userlocation.save();
    return Response(status=status.HTTP_201_CREATED, data=userlocation)
