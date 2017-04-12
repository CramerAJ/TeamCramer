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
    friends = profile.friends.all()
    friend_ids = [f.id for f in friends]
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
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FriendForm()
    
    
    # /rewards_app/friends/ part...
    profiles = Profile.objects.order_by('-name')
    # friends = request.user.inlines.Profile.friends.objects.order_by('-name')
    # print(request.user.username)

    context = {
          'form':form,
          'profiles':profiles,
          'friends':friend_ids,
          'user':friends,
      }

    return render(request, 'rewards_app/friends.html', context)

def index(request):
    u = request.user
    profile = Profile.objects.get(user=u)
    friends = profile.friends.all()
    friend_ids = [f.id for f in friends]
    feed = Activity.objects.filter(profile_id__in=friend_ids).order_by('timestamp')[::-1]
    return render(request, 'rewards_app/home.html', {'feed': feed, 'name': profile.name, 'points': profile.current_points})
