from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.http import Http404

from .models import Post
from .forms import SignUpForm, CreatePostForm

# Create your views here.
@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all().order_by('-created_on')
    
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        user_id = request.POST.get('user-id')

        if post_id:
            post = get_object_or_404(Post, id=post_id)
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    
    context = {
        'posts':posts,
        
    }
    return render(request,'main/home.html',context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))
    else:
        form = SignUpForm()
        return render(request, 'registration/sign_up.html',{'form':form})

@permission_required('main.add_post', login_url='/login', raise_exception=True)
@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('home'))
    else:
        form = CreatePostForm()
    
    return render(request, 'main/create_post_form.html',{'form':form})

@permission_required('main.change_post', login_url='/login', raise_exception=True)
@login_required(login_url='/login')
def edit_post(request,slug):
    post = get_object_or_404(Post,slug=slug)

    if post.author != request.user:
        return Http404("It's not possible my cheif!")
    if request.method == 'POST':
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('home'))
    else:
        form = CreatePostForm(instance=post)
    return render(request, 'main/create_post_form.html', {'form':form})