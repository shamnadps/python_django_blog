from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post,SalesTrackerUser
from .forms import PostForm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from myapp.utils.messages import USER_ALREADY_EXISTS, ERROR_RESP, USER_CREATED
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
    print "inside"
    username = request.GET.get('user', None)
    password = request.GET.get('pass', None)
    phone = request.GET.get('phone', None)
    print "Ok"
    if SalesTrackerUser.objects.filter(phone=phone).exists():
        ERROR_RESP['error']['message'] = USER_ALREADY_EXISTS
        print "error"
        return Response(status=status.HTTP_409_CONFLICT, data=ERROR_RESP)
    else:

        user = SalesTrackerUser(phone,username,password, phone, timezone.now(), 'true');
        user.created_date = timezone.now();
        user.save();

    # Building the response
    USER_CREATED['data']['username'] = username
    USER_CREATED['data']['phone'] = phone
    users = SalesTrackerUser.objects.filter(created_date__lte=timezone.now()).values()
    print username
    print phone
    print users
    print status.HTTP_201_CREATED
    print "All Ok Returning"
    return Response(status=status.HTTP_201_CREATED, data=users)
