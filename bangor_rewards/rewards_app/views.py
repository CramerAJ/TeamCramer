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
    u = request.user
    profile = Profile.objects.get(user=u)
    friendslist = profile.friends.all()
    if request.method == 'POST':
    	print("xdddddddddd")
        # create a form instance and populate it with data from the request:
        form = FriendForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
        	print("valid")

            
        else:
        	form = FriendForm()
    #friend_ids = [f.id for f in friends]
    #feed = Activity.objects.filter(profile_id__in=friend_ids).order_by('timestamp')[::-1]
    context = {
    'form':form,
    'user':u,
    'friendslist':friendslist,
 	 }
    return render(request, 'rewards_app/friends.html', context)

def index(request):
    u = request.user
    profile = Profile.objects.get(user=u)
    friends = profile.friends.all()
    friend_ids = [f.id for f in friends]
    feed = Activity.objects.filter(profile_id__in=friend_ids).order_by('timestamp')[::-1]
    return render(request, 'rewards_app/home.html', {'feed': feed, 'name': profile.name, 'points': profile.current_points})

