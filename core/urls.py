from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('upload',views.upload,name='upload'),
    path('liked_post',views.liked_post,name='liked_post'),
    path('signup',views.signup,name='signup'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('signin',views.signin,name='signin'),
    path('logout',views.logout,name='logout'),
    path('setting',views.setting,name='setting'),
]
