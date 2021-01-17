from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from .models import Profile, Relationship
from .forms import ProfileForm
from posts.models import Post
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def my_profile_view(request):
    posts = Post.objects.all()
    liked = []
    for post in posts:
        for like in post.licked.all():
            liked.append(like)
    profile = Profile.objects.get(user=request.user)
    given_like = liked.count(profile)
    user = request.user
    confirm = False
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {'profile': profile, 'confirm': confirm, 'user': user, 'form': form, 'given_like': given_like}
    return render(request, 'myprofile.html', context)


@login_required
def invite_recieved_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitation_recieved(reciever=profile)
    is_empty = False
    if len(qs) == 0:
        is_empty = True
    senderList = []
    for item in qs:
        senderList.append(item.sender)
    context = {'qs': senderList, 'is_empty': is_empty}
    return render(request, 'invitation.html', context)


@login_required
def get_all_profiles_to_invite(request):
    qs = Profile.objects.get_all_profiles_to_invite(sender=request.user)
    context = {'qs': qs}
    return render(request, 'invitelist.html', context)


@login_required
def get_all_profiles(request):
    profiles = Profile.objects.get_all_profiles(sender=request.user)
    profile = Profile.objects.get(user=request.user)
    rel_r = Relationship.objects.filter(sender=profile)
    rel_s = Relationship.objects.filter(receiver=profile)
    rel_recciever = []
    rel_sender = []
    for obj in rel_r:
        rel_recciever.append(obj.receiver.user)
    for obj in rel_s:
        rel_sender.append(obj.sender.user)
    is_empty = False
    if not profiles:
        is_empty = True

    context = {'rel_recciever': rel_recciever, 'rel_sender': rel_sender, 'profiles': profiles, 'is_empty': is_empty}
    return render(request, 'all-profiles.html', context)


@login_required
def send_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_id')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return request('my-profile')


@login_required
def remove_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_id')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)
        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return request('my-profile')


@login_required
def profile_detail_view(request, **kwargs):
    posts = Post.objects.all()
    liked = []
    for post in posts:
        for like in post.licked.all():
            liked.append(like)
    slug = kwargs['slug']
    profile = Profile.objects.get(slug=slug)
    given_like = liked.count(profile)
    my_profile = Profile.objects.get(user=request.user)
    rel_r = Relationship.objects.filter(sender=my_profile)
    rel_s = Relationship.objects.filter(receiver=my_profile)
    rel_recciever = []
    rel_sender = []
    for obj in rel_r:
        rel_recciever.append(obj.receiver.user)
    for obj in rel_s:
        rel_sender.append(obj.sender.user)
    context = {'profile': profile, 'rel_recciever': rel_recciever, 'rel_sender': rel_sender, 'my_profile': my_profile,
               'given_like': given_like}
    return render(request, 'profile-detail.html', context)


@login_required
def accept_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_id')
        sender = Profile.objects.get(id=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = Relationship.objects.get(sender=sender, receiver=receiver, status='send')
        rel.status = 'accepted'
        rel.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return request('invitation-recieve')


@login_required
def deny_request(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_id')
        sender = Profile.objects.get(id=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = Relationship.objects.get(sender=sender, receiver=receiver, status='send')
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return request('invitation-recieve')


@login_required
def my_friends(request):
    profile = Profile.objects.get(user=request.user)
    relation = Relationship.objects.filter(status='accepted')
    my_friends = []
    for rel in relation:
        if profile.user == rel.sender.user:
            my_friends.append(Profile.objects.get(user=rel.receiver.user))
        if profile.user == rel.receiver.user:
            my_friends.append(Profile.objects.get(user=rel.sender.user))
    context = {
        'my_friends': my_friends
    }
    return render(request, 'my-friends.html', context)
