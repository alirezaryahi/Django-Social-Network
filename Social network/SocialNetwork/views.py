from django.contrib.auth.models import User
from django.shortcuts import render
from profiles.models import Profile, Relationship


def home_view(request):
    context = {
        'user': request.user
    }
    return render(request, 'main/home.html', context)


def SearchFriend(request):
    q = request.GET.get('q')
    user = User.objects.get(username=q)
    profiles = Profile.objects.filter(user=user)
    my_profile = Profile.objects.get(user=request.user)
    rel_r = Relationship.objects.filter(sender=my_profile)
    rel_s = Relationship.objects.filter(receiver=my_profile)
    rel_recciever = []
    rel_sender = []
    for obj in rel_r:
        rel_recciever.append(obj.receiver.user)
    for obj in rel_s:
        rel_sender.append(obj.sender.user)
    is_empty = False
    if not len(profiles):
        is_empty = True
    context = {'profiles': profiles, 'is_empty': is_empty, 'rel_recciever': rel_recciever, 'rel_sender': rel_sender}
    return render(request, 'main/search.html', context)
