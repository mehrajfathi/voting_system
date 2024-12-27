from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('polls/', views.poll_list, name='poll_list'),
    path('polls/create/', views.create_poll, name='create_poll'),
    path('polls/<int:pk>/', views.poll_detail, name='poll_detail'),
    path('polls/<int:pk>/delete/', views.poll_delete, name='poll_delete'),
    path('polls/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('logout/', views.logout_view, name='logout'),
] 