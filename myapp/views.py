from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm

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