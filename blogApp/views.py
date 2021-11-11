from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse,Http404
from blogApp.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import UnauthenticatedUser, allowedUsers

import random
import string
from blogApp.forms import Commentform, createForm, createUserForm,loginUserForm

# Create your views here.
def homePage(request):
    posts_data = Post.objects.all()
    for post in posts_data:
        comments = post.comments_set.all()
        views = post.postview_set.all()
        post.comments = comments.count()
        post.views = views.count()
        # print(post.views)

    
    print(posts_data)
    length = posts_data.count()
    posts_list = list(posts_data)   
    
    posts = random.sample(posts_list,length)
    data = {'posts': posts, 'post_no': length}
    # print(posts)
    return render(request, 'pages/homepage.html', data)

# @UnauthenticatedUser
# @allowedUsers(allowed_roles=['admin','author'])
def createPost(request):  
    user = request.user
    allowed_chars = ''.join((string.ascii_letters, string.digits))
    unique_id = ''.join(random.choice(allowed_chars) for _ in range(8))
    initial = {'post_string':unique_id}
    # print(user)
    form = createForm(initial)
    if (request.method == 'POST'):
        form = createForm(request.POST,request.FILES)        
        if form.is_valid():
            form.save()
            messages.success(request, 'New post was created successfully')
            return redirect('/') 

    data = {
        'form':form
    }
    return render(request, 'pages/create-post.html', data)

# @UnauthenticatedUser
# @allowedUsers(allowed_roles=['admin','author'])
def updatePost(request, id):
    post = Post.objects.get(id=id)   
    form = createForm(instance=post)
    if (request.method == 'POST'):
        form = createForm(request.POST,request.FILES, instance=post)        
        if form.is_valid():
            form.save()
            messages.success(request, 'post updated successfully')

            return redirect('/') 
    else:
        if (post.author == request.user):
            data = {
                'form':form
            }
            # return render(request, 'pages/create-post.html', data)
            return render(request, 'pages/update-post.html', data)
        else:
            return HttpResponse('<h1 class="text-danger"> sorry! You are not authorised to edit this page </h1>')

# @UnauthenticatedUser
# @allowedUsers(allowed_roles=['admin','author'])
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    print(post)
    data = {'item': post}
    if (request.method == 'POST'):       
            post.delete()
            messages.success(request, 'post was deleted successfully')
            return redirect('/')
    else:
        if (post.author == request.user):
            
            # return render(request, 'pages/create-post.html', data)
            return render(request,'pages/delete-post.html', data)
        else:
            return HttpResponse('<h1 class="text-danger"> sorry! You are not authorised to Delete this page </h1>')
    

def details(request, id):
    post = get_object_or_404(Post,pk=id)
    auth_user_name = request.user.username
    post_id = id
    url = visited(request)
    # print(post.author)

    # print(request.user)    
    views_add(post,url)
    initial = {
            'post_id': post_id,
            'user_name': auth_user_name
        }
    form = Commentform(initial)
    post = Post.objects.get(id=post_id)
    comments = get_comments(post)
     
    
    
    category = Category.objects.filter(id=post.id)
    # print (category)
    comments_no =  comments.count()
    views = PostView.objects.filter(post_id=id)
    views_no = views.count()
       

    # print(views)
    data = {
        'post': post,
        'category': category,
        'comments': comments,
        'comments_no': comments_no,
        'form': form,
        'views_no': views_no
        }

    # print(comments_no)
   
    return render(request,'pages/details.html', data)

def get_comments(post):
    data = post.comments_set.all().order_by('-created_at')   
    return data

# @login_required(login_url='ur'l)
def logoutUser(request):
    logout(request)
    return redirect('login')

@UnauthenticatedUser   
def loginUser(request):
    form = loginUserForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user)
            login(request, user)
            # messages.success(request, 'user logged in successfully')
            return redirect('home')
        else:
            print('failed')
            messages.warning(request, 'usename or password is incorect')
            return render(request, 'pages/login.html')
    context = {
        'form':form
    }

    return render(request, 'pages/login.html',context)
# @UnauthenticatedUser
# @allowedUsers(allowed_roles=['admin','author', 'visitor'])
def userProfile(request):
    auth_user = request.user
    print(auth_user.profile.image_profile)
    data = {
        'auth_user':auth_user
    }
    return render(request,'pages/user-profile.html', data)

def register(request):
    form = createUserForm()    
    if request.method == 'POST':
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='visitor')
            user.groups.add(group)
            return redirect('login')
    data = {
        'form':form 
    }
    return render(request, 'pages/register.html', data)
    

def views_add(post_id, post_url):
    PostView.objects.create(post_id=post_id, post_url=post_url)
    # PostView.save()

def visited(request):
    current = request.get_full_path()
    url = request.META.get('HTTP_REFERER')
    return current

# @allowedUsers(allowed_roles=['admin','author', 'visitor'])
def addComment(request):
    if(request.method == 'POST'):
        postComment = Commentform(request.POST) 
        
        # current = visited(request) 
        url = request.META.get('HTTP_REFERER')
         # print(  url )
        if postComment.is_valid():
            postComment.save()
            messages.success(request, 'your comment was recived successfully')
        return redirect( url ) 
    else:
        messages.info(request, 'your comment was not able to submit, please try again later')


# @UnauthenticatedUser
# @allowedUsers(allowed_roles=['author'])
def userDashbord(request):
    auth_user = request.user
    my_posts = Post.objects.filter(author=auth_user) 
    post_no = my_posts.count()
    for my_post in my_posts:
        my_post.comments_no = my_post.comments_set.all().count()
        my_post.views_no = my_post.postview_set.all().count()
        
    data = {'my_posts':my_posts, 'post_no':post_no } 
    # print(my_posts)
    return render(request, 'pages/user-dashboard.html',data)