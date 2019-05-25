from django.urls import path
from . import views

app_name = 'CurveApp'

urlpatterns=[
    path('', views.index, name='index'),
    path('(?P<album_id>[0-9]+)/', views.detail, name='detail'),
    path('signup', views.signup, name='signup'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='logout'),
    path('create-album', views.create_album, name='create-album'),
    path('(?P<album_id>[0-9]+)/create-song', views.create_song, name='create-song'),
    path('(?P<album_id>[0-9]+)/delete-album', views.delete_album, name='delete-album'),
    path('<int:pk>/update-album', views.AlbumUpdateView.as_view(), name='update-album'),
    path('(?P<album_id>[0-9]+)/delete-song/(?P<song_id>[0-9]+)/', views.delete_song, name='delete-song'),
    path('profile/(?P<user_id>[0-9]+)/', views.profile_view, name='profile'),
]