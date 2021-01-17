from django.urls import path
from .views import my_profile_view, invite_recieved_view, get_all_profiles_to_invite, get_all_profiles, send_request, \
    remove_friend, profile_detail_view, accept_request, deny_request, my_friends

urlpatterns = [
    path('', my_profile_view, name='my-profile'),
    path('my-invites/', invite_recieved_view, name='invitation-recieve'),
    path('invite-list/', get_all_profiles_to_invite, name='invite-list'),
    path('all-profiles/', get_all_profiles, name='all-profiles-list'),
    path('send-request/', send_request, name='send-request'),
    path('remove-friend/', remove_friend, name='remove-friend'),
    path('accept-request/', accept_request, name='accept-request'),
    path('deny-request/', deny_request, name='deny-request'),
    path('my-friends/', my_friends, name='my-friends'),
    path('<slug>/', profile_detail_view, name='profile-detail'),
]
