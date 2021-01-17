from django.contrib import admin
from .models import Profile, Relationship


# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'create']

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Relationship)
