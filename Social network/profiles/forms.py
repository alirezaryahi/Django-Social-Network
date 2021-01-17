from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 10}))
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'country', 'avatar')
