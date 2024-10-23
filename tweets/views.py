from django.shortcuts import render
from .models import Tweets
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import TweetForm, LoginForm

def index(req):
    tweets = Tweets.objects.all().order_by('-created_at')
    return render(req, 'list.html', {'tweets' : tweets})

def register(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(req, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(req, 'registration/register.html', {'form' : form})

@login_required
def create(req):
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            return redirect('index')
    else:
        form = TweetForm()
    return render(req, 'create.html', {'form' : form})
    
@login_required
def update(req, tid):
    tweet = get_object_or_404(Tweets, pk=tid, user = req.user)
    if req.method == 'POST':
        form = TweetForm(req.POST, req.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = req.user
            tweet.save()
            return redirect('index')
    else:
        form = TweetForm(instance=tweet)
        return render(req, 'create.html', {'form' : form})

@login_required
def delete(req, tid):
    tweet = get_object_or_404(Tweets, pk = tid, user = req.user)
    tweet.delete()    
    return redirect('index')