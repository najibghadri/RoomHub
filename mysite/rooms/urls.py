from django.urls import path,include
from django.views.generic.base import TemplateView

from . import views

app_name = 'rooms'
urlpatterns = [
    path('', views.EventList.as_view(), name='home'),
    path('password/', views.change_password, name='change_password'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/edit', views.EditProfile.as_view(), name='edit_profile'),
    path('events/new', views.EventCreate.as_view(), name='event_new'),
    path('events/<int:pk>/', views.EventDetail.as_view(), name='event_detail'),
    path('events/<int:pk>/edit/', views.EventEdit.as_view(), name='event_edit'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='event_delete'),
    path('my-events/',views.MyEventList.as_view(), name='my_events'),
    path('rooms/',views.RoomList.as_view(), name='rooms'),
    path('rooms/new/', views.RoomCreate.as_view(), name='room_create'),
    path('rooms/<int:pk>/edit/', views.RoomEdit.as_view(), name='room_edit'),
    path('rooms/<int:pk>/delete/', views.RoomDelete.as_view(), name='room_delete'),

]
