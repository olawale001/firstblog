from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_new, name='post_new'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.login_view, name='login'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete', views.post_delete, name='post_delete'),
    path('logout/', views.logout_user, name='logout'),
    path('post/<int:pk>/comment/add/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_pk>/reply/', views.add_reply, name='add_reply'),
    path('comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('reply/<int:reply_pk>/delete/', views.reply_delete, name='reply_delete'),
   
]