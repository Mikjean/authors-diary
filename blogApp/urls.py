from django.urls import path
from . import views


urlpatterns = [
    path('', views.homePage,name='home'),
    path('new-post/', views.createPost, name='new-post'),
    path('update-post/<str:id>', views.updatePost, name='update-post'),
    path('delete-post/<str:pk>', views.deletePost, name='delete-post'),
    path('details/<str:id>', views.details, name='details'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('comment/add/', views.addComment, name='add-comment'),
    path('auth/user/profile/', views.userProfile, name='user-profile'),
    path('auth/user/dashboard/', views.userDashbord, name='user-dashboard'),

    

]
