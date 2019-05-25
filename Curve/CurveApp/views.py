from django.shortcuts import render, get_object_or_404, redirect
from .models import Album, Song, User
from . import forms 
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView

# Create your views here.

#Registering new users
def signup(request):
    form = forms.UserForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = form.save(commit=False)
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            context = {
                'message' : 'Welcome' ,
            }
            return render(request, 'CurveApp/index.html', context)
            
    return render(request, 'registration/signup.html', {'form':form})

@login_required(login_url='CurveApp:login')
def index(request):
    album = Album.objects.all
    return render(request, 'CurveApp/index.html', {'album':album})
    
# Displays all albums
@login_required(login_url='CurveApp:login')
def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'CurveApp/detail.html', {'album':album})

# This view filters albums to display albums only for a particular requested user
@login_required(login_url='CurveApp:login')
def profile_view(request, user_id):
    requesteduser =  get_object_or_404(User, pk=user_id)
    album = Album.objects.filter(user=requesteduser)
    context = {
        'album' : album,
        'user' : requesteduser,
    }
    return render(request, 'CurveApp/index.html', context)
    
#Logging in users    
def signin(request):
    if request.method == 'POST':
        username = request.POST['uid']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('CurveApp:index')
    return render(request, 'registration/login.html')

#Logging out
@login_required(login_url='CurveApp:login')
def signout(request):
    logout(request)
    return redirect('CurveApp:login')

@login_required(login_url='CurveApp:login')
def create_album(request):
    form = forms.AlbumForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        myalbum = Album.objects.filter(user=request.user)
        for album in myalbum:
            if album.album_name == form.cleaned_data.get('album_name'):
                context = {
                    'message' : 'You already added this album',
                    'album' : myalbum,
                    'msgtype' : 'danger',
                }
                return render(request, 'CurveApp/index.html', context)
            
        album = form.save(commit=False)
        album.album_cover = request.FILES['album_cover']
        album.user = request.user
        album.save()
        context = {
            'album' : myalbum,
            'message' : 'You have added an album to your collection',
            'msgtype' : 'success',
        }
        return render(request, 'CurveApp/index.html', context)
    return render(request, 'CurveApp/create_album.html', {'form':form})

@login_required(login_url='CurveApp:login')
def create_song(request, album_id):
    form = forms.SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        for song in album.song_set.all():
            if song.song_name == form.cleaned_data.get('song_name'):
                context = {
                    'album' : album,
                    'message' : 'The song is already added',
                    'msgtype' : 'danger',
                }
                return render(request, 'CurveApp/detail.html', context)
        song = form.save(commit=False)
        song.album = album
        song.song_artist = album.album_artist
        song.song = request.FILES['song']
        song.save()
        context = {
            'album': album,
            'message':'Song added successfully.'
        }
        return render(request, 'CurveApp/detail.html', context)
    return render(request, 'CurveApp/create-song.html', {'form':form})

@login_required(login_url='CurveApp:login')
def delete_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    album.delete()
    return redirect('/')


class AlbumUpdateView(UpdateView):
    model = Album
    fields = ['album_name', 'album_artist', 'album_cover']
    template_name = 'CurveApp/create_album.html'

@login_required(login_url='CurveApp:login')
def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = get_object_or_404(Song, pk=song_id)
    song.delete()
    context = {
        'album' : album,
        'message' : 'Song deleted successfully.',
    }
    return render(request, 'CurveApp/detail.html', context)