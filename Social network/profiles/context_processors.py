from .models import Profile, Relationship


def profile_pic(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        pic = profile.avatar
        return {'picture': pic}
    return {}


def invite_number(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        invite_count = Relationship.objects.invitation_recieved(profile).count()
        return {'invite_count': invite_count}
    return {}


def friends_number(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        number = profile.friends.all().count()
        return {'friends_number': number}
    return {}
