from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Charity
from .models import Activity
from .models import Profile
from .forms import FriendForm


# Shows list of charities in DB
"""def index(request):
    latest_charity_list = Charity.objects.order_by('-name')[:5]
    context = {'latest_charity_list': latest_charity_list}
    return render(request, 'rewards_app/index.html', context)"""


#forms tutorial...
def add_friend(request):
    profiles = None
    friends = None
	# /rewards_app/add_friend/ part...
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FriendForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # print("FRIEND FORM IS HERE::"+form.errors.as_data())
            
            if (not request.POST.get("search")):
                name = request.POST.getlist("add")[0][4:]
                newFriend = Profile.objects.filter(name=name).get()
                u = request.user
                p = Profile.objects.get(user=u)
                p.friends.add(newFriend)
            
            name = form.cleaned_data['friend_name']
            u = Profile.objects.get(user=request.user)
            profiles = Profile.objects.filter(name__contains=name).exclude(user=request.user)
            for f in u.friends.all():
                profiles = profiles.exclude(pk=f.pk)


    # if a GET (or any other method) we'll create a blank form
    else:
        form = FriendForm()


    # /rewards_app/friends/ part...
    #profiles = Profile.objects.order_by('-name')
    # friends = request.user.inlines.Profile.friends.objects.order_by('-name')
    # print(request.user.username)
    u = request.user
    profile = Profile.objects.get(user=u)
    friends = profile.friends.all()

    context = {
          'form':form,
          'profiles':profiles,
          'friends':friends,
      }

    return render(request, 'rewards_app/FriendsTest.html', context)
    #return render(request, 'rewards_app/friends.html', context)

def charities(request):
    u = request.user
    profile = Profile.objects.get(user=u)

    charities = Charity.objects.order_by('-points')

    return render(request, 'rewards_app/Charities.html', {'charities': charities, 'profile': profile})


def leaderboard(request):
    u = request.user
    profile = Profile.objects.get(user=u)
    friends = profile.friends.all()
    friend_ids = [f.id for f in friends]
    userList = Profile.objects.order_by('-total_points')
    #Get list of top 10 friends by total points
    friendBoard = Profile.objects.filter(id__in=friend_ids).order_by('-total_points')[:10]
    #Get list of top 10 users by total points
    userBoard = Profile.objects.order_by('-total_points')[:10]
    #Get list of top 10 charities by total points
    charityBoard = Charity.objects.order_by('-points')[:10]
    return render(request, 'rewards_app/LeaderboardTabs.html', {'userList': userList, 'profile': profile, 'friendBoard': friendBoard, 'userBoard': userBoard, 'charityBoard': charityBoard})

def profile(request):
    u = request.user
    profile = Profile.objects.get(user=u)
    achievements = profile.achievements.all()
    return render(request, 'rewards_app/profile.html',{'profile': profile, 'achievements' : achievements})

def index(request):
    u = request.user
    profile = Profile.objects.get(user=u)
    friends = profile.friends.all()
    friend_ids = [f.id for f in friends]
    feed = Activity.objects.filter(profile_id__in=friend_ids).order_by('timestamp')[::-1]
    return render(request, 'rewards_app/home.html', {'feed': feed, 'name': profile.name, 'points': profile.current_points, 'profile': profile})
